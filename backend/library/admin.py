from django.contrib import admin
from .models import User, Book, Loan, Reservation, Category
# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Reservation)
admin.site.register(Category)