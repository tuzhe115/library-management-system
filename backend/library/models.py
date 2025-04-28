from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
import requests

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=32, verbose_name="Name")

    account = models.CharField(max_length=32, verbose_name="Account")

    email = models.EmailField(max_length=64, verbose_name="Email")

    password = models.CharField(max_length=32, verbose_name="Password")

    phone = models.CharField(max_length=32, verbose_name="Phone")

    role = models.CharField(max_length=32, verbose_name="Role")

    borrow_duration = models.IntegerField(verbose_name="Borrow Duration")

    borrow_num = models.IntegerField(verbose_name="Borrow Number")

    reservation_duration = models.IntegerField(verbose_name="Reservation Duration")

    registration_time = models.DateTimeField(auto_now_add=True, verbose_name="Registration Time")

    address = models.CharField(max_length=255, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)

    longitude = models.FloatField(blank=True, null=True)

    # Save latitude and longitude got from get_coordinates_from_address()
    def save(self, *args, **kwargs):
        if self.address:
            self.latitude, self.longitude = self.get_coordinates_from_address(self.address)
        super().save(*args, **kwargs)

    # Return latitude and longitude of the input address
    def get_coordinates_from_address(self, address):
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
        headers = {
            "User-Agent": "library-system/1.0 (misaki102443@gmail.com)"
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except Exception as e:
            print(f"Geocoding failed: {e}")
        return None, None

    def __str__(self):
        return self.name

    class Meta:
        db_table = "lib_user"


# Category class
class Category(models.Model):
    id = models.AutoField(primary_key=True)

    category_name = models.CharField(max_length=64, verbose_name="Category")

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category"

# Book class
class Book(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=32)

    author = models.CharField(max_length=32)

    ISBN = models.CharField(max_length=64, verbose_name="ISBN")

    publisher = models.CharField(max_length=32, verbose_name="Publisher")

    published_year = models.IntegerField(verbose_name="Published Year", validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)])

    price = models.DecimalField(max_digits = 5, decimal_places=2)

    total_copies = models.IntegerField(verbose_name="Total Copies")

    available_copies = models.IntegerField(verbose_name="Available Copies")

    category = models.ManyToManyField(Category)

    # Display of book title in foreign table
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'book'

# Loan class
class Loan(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    borrow_time = models.DateTimeField(auto_now_add=True, verbose_name="Borrow Time")

    due_time = models.DateTimeField(blank=True, null=True,verbose_name="Due Time")

    return_time = models.DateTimeField(blank=True, null=True,verbose_name="Return Time")

    loan_status = models.CharField(max_length=32, default='Active',verbose_name="Loan Status")

    # Auto due time calculation
    def save(self, *args, **kwargs):
        if not self.borrow_time:
            self.borrow_time = timezone.now()
        if not self.due_time:
            self.due_time = self.borrow_time + timedelta(days=self.user.borrow_duration)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'loan'

# Reservation class
class Reservation(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    reservation_time = models.DateTimeField(auto_now_add=True, verbose_name="Reservation Time")

    r_due_time = models.DateTimeField(blank=True, null=True,verbose_name="Reservation Due Time")

    reservation_status = models.CharField(max_length=32, verbose_name="Reservation Status")

    # Auto reservation due time calculation
    def save(self, *args, **kwargs):
        if not self.reservation_time:
            self.reservation_time = timezone.now()
        if not self.r_due_time:
            self.r_due_time = self.reservation_time + timedelta(days=self.user.reservation_duration)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'reservation'

# Fine class
class Fine(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits = 5, decimal_places=2, verbose_name="Amount")

    fine_status = models.CharField(max_length=32, verbose_name="Fine Status")

    issued_time = models.DateTimeField(auto_now_add=True, verbose_name="Issued Time")

    class Meta:
        db_table = 'fine'