from django.shortcuts import render
from rest_framework import viewsets,filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime
from django.urls import path, include
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.decorators import api_view
from collections import Counter
from django.utils.timezone import now

from .models import Book, User, Loan, Fine, Reservation, Category
from .serializers import (
    BookSerializer, UserSerializer, LoanSerializer,
    FineSerializer, ReservationSerializer, CategorySerializer
)

# ViewSet for Book model
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']

    # Search
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        field = self.request.query_params.get('field')
        if keyword and field:
            if field == 'category':
                queryset = queryset.filter(category__category_name__icontains=keyword)
            elif field == 'published_year':
                queryset = queryset.filter(published_year__icontains=keyword)
            elif field in ['title', 'author', 'ISBN', 'publisher']:
                filter_key = f"{field}__icontains"
                queryset = queryset.filter(**{filter_key: keyword})
        return queryset

# ViewSet for Category model
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# ViewSet for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    # Search
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        field = self.request.query_params.get('field')
        if keyword and field:
            if field in ['name','account', 'email', 'phone', 'role', 'address']:
                filter_key = f"{field}__icontains"
                queryset = queryset.filter(**{filter_key: keyword})
        return queryset


# ViewSet for Loan model
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('id')
    serializer_class = LoanSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['loan_status']

    # Search
    def get_queryset(self):
        queryset = super().get_queryset()

        # Auto update overdue status
        now = timezone.now()
        overdue_loans = queryset.filter(
            Q(return_time__isnull=True) &
            Q(due_time__lt=now) &
            ~Q(loan_status='overdue')
        )
        overdue_loans.update(loan_status='overdue')

        keyword = self.request.query_params.get('keyword')
        field = self.request.query_params.get('field')
        if keyword and field:
            if field == 'book_title':
                queryset = queryset.filter(book__title__icontains=keyword)
            elif field == 'user_name':
                queryset = queryset.filter(user__name__icontains=keyword)
            elif field == 'loan_status':
                queryset = queryset.filter(loan_status__icontains=keyword)
        return queryset

    # Add loan auto available copies -1, if available copies<1, can't add loan
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        if not book_id:
            raise ValidationError({'book': 'Book is required.'})

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise ValidationError({'book': 'Book not found.'})

        if book.available_copies < 1:
            raise ValidationError({'book': 'No available copies left for this book.'})

        response = super().create(request, *args, **kwargs)

        book.available_copies -= 1
        book.save()

        return response

    # Return book and available copies + 1
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        previous_return_time = instance.return_time

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        if updated_instance.return_time and not previous_return_time:
            book = updated_instance.book
            book.available_copies += 1
            book.save()

        return Response(serializer.data)

    # Restrict borrowing books if borrow limit is reached
    def perform_create(self, serializer):
        user = serializer.validated_data['user']
        active_loans = Loan.objects.filter(user=user, return_time__isnull=True).count()

        if active_loans >= user.borrow_num:
            raise ValidationError({"user": "Borrowing limit reached."})

        serializer.save()

# ViewSet for Fine model
class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer

# ViewSet for Reservation model
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by('id')
    serializer_class = ReservationSerializer

    # Search
    def get_queryset(self):
        queryset = super().get_queryset()

        # Auto update expired status
        now = timezone.now()
        expired_reservation = queryset.filter(
            Q(r_due_time__lt=now) &
            ~Q(reservation_status='expired')
        )
        for reservation in expired_reservation:
            reservation.reservation_status = 'expired'
            reservation.save()

            book = reservation.book
            book.available_copies += 1
            book.save()

        keyword = self.request.query_params.get('keyword')
        field = self.request.query_params.get('field')
        if keyword and field:
            if field == 'book_title':
                queryset = queryset.filter(book__title__icontains=keyword)
            elif field == 'user_name':
                queryset = queryset.filter(user__name__icontains=keyword)
            elif field == 'reservation_status':
                queryset = queryset.filter(reservation_status__icontains=keyword)
        return queryset

    # Auto available copies-1 when adding reservation
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        if not book_id:
            raise ValidationError({'book': 'Book is required.'})

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise ValidationError({'book': 'Book not found.'})

        if book.available_copies < 1:
            raise ValidationError({'book': 'No available copies left for this book.'})

        response = super().create(request, *args, **kwargs)

        book.available_copies -= 1
        book.save()

        return response

    # Auto +1 for available copies when status is changed to cancelled or expired
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        previous_status = instance.reservation_status

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_reservation = serializer.save()

        if (
                updated_reservation.reservation_status in ["cancelled", "expired"]
                and previous_status != updated_reservation.reservation_status
        ):
            book = updated_reservation.book
            book.available_copies += 1
            book.save()

        return Response(serializer.data)

# Statistics View
class StatisticsViewSet(viewsets.ViewSet):

    # API to get user role distribution
    @action(detail=False, methods=['get'])
    def user_role_distribution(self, request):
        users = User.objects.all()
        role_counts = Counter(user.role for user in users)

        data = [{"name": role.capitalize(), "value": count} for role, count in role_counts.items()]

        return Response(data)

    # API to get monthly user registration counts and monthly active users based on loans
    @action(detail=False, methods=['get'])
    def user_growth_statistics(self,request):
        now = datetime.now()
        six_months_ago = now - timedelta(days=180)

        # Count total registered users per month
        total_users = (
            User.objects.all()
            .annotate(month=TruncMonth('registration_time'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Count active users (users who borrowed books) per month
        active_users = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month')
            .annotate(count=Count('user', distinct=True))
            .order_by('month')
        )

        # Prepare response data
        months = []
        total_counts = []
        active_counts = []

        month_set = sorted(set([item['month'] for item in total_users] + [item['month'] for item in active_users]))

        for month in month_set:
            months.append(month.strftime("%Y-%m"))
            total_count = next((item['count'] for item in total_users if item['month'] == month), 0)
            active_count = next((item['count'] for item in active_users if item['month'] == month), 0)
            total_counts.append(total_count)
            active_counts.append(active_count)

        return Response({
            "months": months,
            "total_users": total_counts,
            "active_users": active_counts,
        })

    # API to get monthly average borrow numbers in total and by user role
    @action(detail=False, methods=['get'])
    def user_borrow_statistics(self, request):

        now = datetime.now()
        six_months_ago = now - timedelta(days=180)

        # 1. Total borrows per month
        loans = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month')
            .annotate(total_borrows=Count('id'))
            .order_by('month')
        )

        # 2. Borrow count by user role per month
        role_borrows = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month', 'user__role')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Prepare response
        months = sorted(set([item['month'] for item in loans]))
        month_labels = [m.strftime("%Y-%m") for m in months]

        total_borrows_per_month = []
        role_data = {
            "Undergraduate": [],
            "Postgraduate": [],
            "Doctor": [],
            "Professor": []
        }

        for month in months:
            total = next((item['total_borrows'] for item in loans if item['month'] == month), 0)
            total_borrows_per_month.append(total)
            for role in role_data.keys():
                role_count = next(
                    (item['count'] for item in role_borrows if item['month'] == month and item['user__role'] == role), 0
                )
                role_data[role].append(role_count)

        return Response({
            "months": month_labels,
            "total_borrows": total_borrows_per_month,
            "undergraduate": role_data["Undergraduate"],
            "postgraduate": role_data["Postgraduate"],
            "doctor": role_data["Doctor"],
            "professor": role_data["Professor"],
        })

    # API to get monthly total number of books and monthly number of books loaned
    @action(detail=False, methods=['get'])
    def book_growth_statistics(self, request):

        now = datetime.now()
        six_months_ago = now - timedelta(days=180)

        total_books = Book.objects.count()

        # Count monthly loans
        loans = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        months = []
        borrow_counts = []
        # Collect months
        for record in loans:
            months.append(record['month'].strftime("%Y-%m"))
            borrow_counts.append(record['count'])

        return Response({
            "total_books": total_books,
            "months": months,
            "borrowed_books": borrow_counts
        })

    # API to get distribution of books across categories
    @action(detail=False, methods=['get'])
    def book_category_distribution(self, request):

        books = Book.objects.all()
        category_counter = Counter()

        for book in books:
            for category in book.category.all():
                category_counter[category.category_name] += 1

        data = [
            {"name": name, "value": count}
            for name, count in category_counter.items()
        ]

        return Response(data)


    # API to get distribution of borrowed book categories over the past 6 months
    @action(detail=False, methods=['get'])
    def monthly_borrowed_category_distribution(self, request):
        today = now()
        six_months_ago = today - timedelta(days=180)

        # Get all loans from the past 6 months
        loans = Loan.objects.filter(borrow_time__gte=six_months_ago).select_related('book').prefetch_related(
            'book__category')

        monthly_category_counter = {}
        for loan in loans:
            if loan.book:
                month = loan.borrow_time.strftime('%Y-%m')
                if month not in monthly_category_counter:
                    monthly_category_counter[month] = Counter()
                for category in loan.book.category.all():
                    monthly_category_counter[month][category.category_name] += 1

        # Format the response
        response_data = []
        for month, counter in monthly_category_counter.items():
            month_data = {
                "month": month,
                "categories": [{"name": name, "value": count} for name, count in counter.items()]
            }
            response_data.append(month_data)
        return Response(response_data)

    # API to get the top 3 popular categories and top 3 popular books
    @action(detail=False, methods=['get'])
    def top_categories_and_books(self, request):
        now = datetime.now()
        six_months_ago = now - timedelta(days=180)

        # Top 3 categories per month
        from library.models import Loan, Book, Category

        category_data = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month', 'book__category__category_name')
            .annotate(count=Count('id'))
            .order_by('month', '-count')
        )

        # Top 3 books per month
        book_data = (
            Loan.objects.filter(borrow_time__gte=six_months_ago)
            .annotate(month=TruncMonth('borrow_time'))
            .values('month', 'book__title')
            .annotate(count=Count('id'))
            .order_by('month', '-count')
        )

        result = {}
        for item in category_data:
            month = item['month'].strftime('%Y-%m')
            if month not in result:
                result[month] = {'categories': [], 'books': []}
            if len(result[month]['categories']) < 3:
                result[month]['categories'].append(
                    {'name': item['book__category__category_name'], 'count': item['count']})

        for item in book_data:
            month = item['month'].strftime('%Y-%m')
            if month not in result:
                result[month] = {'categories': [], 'books': []}
            if len(result[month]['books']) < 3:
                result[month]['books'].append({'name': item['book__title'], 'count': item['count']})

        return Response(result)
# Register all viewsets using DefaultRouter
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'fines', FineViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'statistics', StatisticsViewSet, basename='statistics')

# URL patterns to include in your project's urls.py
urlpatterns = [
    path('api/', include(router.urls)),
]

# Create your views here.
