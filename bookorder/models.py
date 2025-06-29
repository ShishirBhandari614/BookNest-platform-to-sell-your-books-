# from re import A
from django.db import models
from authentication.models import CustomUser
from django.conf import settings

class Book(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books' )
    book_cover = models.ImageField(upload_to='book_covers/')
    book_name = models.CharField(max_length=255)
    book_description = models.TextField()
    genres = models.CharField(max_length=255)  # Store genres as a comma-separated string
    book_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    author = models.CharField(max_length=255, default='Unknown Author')  # Provide a default value
    publication_date = models.DateField(null=True, blank=True)
    sold = models.BooleanField(default=False)
    available_quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(
        max_length=10,
        choices=[('New', 'New'), ('Old', 'Old')],
        default='Old'
    )


    def __str__(self):
        return self.book_name


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.book_name} x {self.quantity}"

from django.db import models

class CheckoutAddress(models.Model):
    DELIVERY_CHOICES = [
        ('ship', 'Ship'),
        ('pickup', 'Pickup in Store'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Card Payment'),
        ('esewa', 'Esewa'),
    ]

    email = models.EmailField()
    delivery_option = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    country = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    address_type = models.CharField(max_length=10, choices=[('shipping', 'Shipping'), ('billing', 'Billing')])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_type} - {self.first_name} {self.last_name}"
