# from re import A
from django.db import models
from authentication.models import CustomUser


class Book(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='books' )
    book_cover = models.ImageField(upload_to='book_covers/')
    book_name = models.CharField(max_length=255)
    book_description = models.TextField()
    genres = models.CharField(max_length=255)  # Store genres as a comma-separated string
    book_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    author = models.CharField(max_length=255, default='Unknown Author')  # Provide a default value
    publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.book_name