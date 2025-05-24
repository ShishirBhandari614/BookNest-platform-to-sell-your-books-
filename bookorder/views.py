from ast import Pass
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer, AddToCartSerializer
from .models import Book, Cart, CartItem
from rest_framework import status
from django.http import HttpResponseForbidden, JsonResponse
from authentication.authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated

class AddBookView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_seller:
            return HttpResponseForbidden("You are not authorized to access this page.")
        serializer = BookSerializer()
        return render(request, 'bookorder/add_book.html', {'serializer': serializer})

    def post(self, request):
        # Use request.data and request.FILES separately
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response({'msg': 'Data Created', 'success': True})
        return Response({'errors': serializer.errors, 'success': False})
    


class EditBookView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not request.user.is_seller:
            return HttpResponseForbidden("You are not authorized to access this page.")
        
        book = get_object_or_404(Book, pk=pk, seller=request.user)
        genres_list = book.genres.split(',')
        print (genres_list)
        serializer = BookSerializer(instance=book)
        return render(request, 'bookorder/edit_book.html', {'serializer': serializer, 'book': book, 'genres': genres_list})

    def post(self, request, pk):
        if not request.user.is_seller:
            return HttpResponseForbidden("You are not authorized to perform this action.")
        
        book = get_object_or_404(Book, pk=pk, seller=request.user)
        data = request.data.copy()
        if not request.FILES.get('book_cover'):
            data['book_cover'] = book.book_cover
        serializer = BookSerializer(instance=book, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Book updated successfully', 'success': True})
        return Response({'errors': serializer.errors, 'success': False})

class SellerBooksView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_seller:
           return HttpResponseForbidden("You are not authorized to access this page.")
        # Get books uploaded by the current user
        books = Book.objects.filter(seller=request.user).select_related('seller')
        return render(request, 'bookorder/book_sellerwise.html', {'books': books})
    
    
class DeleteBookView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            if not request.user.is_seller:
                return HttpResponseForbidden("You are not authorized to access this page.")
            book = Book.objects.get(id=book_id, seller=request.user)
            book.delete()
            return JsonResponse({'success': True, 'message': 'Book deleted successfully'})
            
        except Book.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Book not found or permission denied'}, status=404)
        
        
class BuyBookView(APIView):
    Pass
    

def count_cart_items():
    return CartItem.objects.count()
  
class AddToCartView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.user.is_buyer:
            return HttpResponseForbidden("You are not authorized to access this page.")
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            quantity = serializer.validated_data['quantity']
            book = Book.objects.get(id=book_id)
            
               

            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            return Response({'message': 'Book added to cart'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)