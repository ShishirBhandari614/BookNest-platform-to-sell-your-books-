from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_cover', 'book_name', 'book_description', 'genres','book_price', 'author', 'publication_date']