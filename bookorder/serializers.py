from rest_framework import serializers
from .models import Book, CartItem

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Includes all model fields
        
    def __init__(self, *args, **kwargs):
        # 1. Initialize parent class first
        super().__init__(*args, **kwargs)
        
        # 2. Check if we're creating new instance (no existing instance)
        if not self.instance:
            # 3. Enforce required cover for new books
            self.fields['book_cover'].required = True
            
class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity']


class AddToCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)