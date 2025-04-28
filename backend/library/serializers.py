from rest_framework import serializers
from .models import Book, User, Loan, Fine, Reservation, Category

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category_name']

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'ISBN', 'publisher',
            'published_year', 'price', 'total_copies',
            'available_copies', 'category', 'category_names'
        ]

    def get_category_names(self, obj):
        return [cat.category_name for cat in obj.category.all()]

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Serializer for the Loan model
class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # submit user.id
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # Book ID input
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    return_time = serializers.DateTimeField(
        input_formats=['%d-%m-%Y %H:%M:%S'], 
        format='%d-%m-%Y %H:%M:%S',
        required=False
    )

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'borrow_time', 'due_time', 'return_time','loan_status','book_title', 'user_name']
# Serializer for the Reservation model
class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # submit user.id
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())  # Book ID input
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'book', 'reservation_time', 'r_due_time','reservation_status', 'book_title', 'user_name']


# Serializer for the Fine model
class FineSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    user = UserSerializer(read_only=True)  # user

    class Meta:
        model = Fine
        fields = '__all__'
