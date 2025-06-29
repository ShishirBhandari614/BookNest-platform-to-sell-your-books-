from ast import Pass
from django.contrib.auth.admin import User
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import BookSerializer, AddToCartSerializer, BookSuggestionSerializer
from .models import Book, Cart, CartItem
from rest_framework import status, permissions
from django.http import HttpResponseForbidden, JsonResponse
from authentication.authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from authentication.views import count_cart_items
from django.views import View
from django.shortcuts import render
from .models import Cart, CartItem
from django.db.models import Sum

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
        print("Validation Errors:", serializer.errors)
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
    




class AddToCartView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_buyer:
            return HttpResponseForbidden("You are not authorized to access this page.")
        
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            requested_quantity = serializer.validated_data['quantity']

            book = get_object_or_404(Book, id=book_id)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

            existing_quantity = cart_item.quantity if not created else 0
            max_addable = book.available_quantity - existing_quantity

            if max_addable <= 0:
                return Response(
                    {
                        'message': 'Book is already added up to available stock.',
                        'cart_count': cart.items.count(),
                        'added_quantity': 0,
                        'existing_quantity': existing_quantity
                    },
                    status=status.HTTP_200_OK
                )

            quantity_to_add = min(requested_quantity, max_addable)
            cart_item.quantity = existing_quantity + quantity_to_add
            cart_item.save()

            message = (
                'Book added to cart.'
                if quantity_to_add == requested_quantity else
                f'Only {quantity_to_add} of {requested_quantity} added due to stock limits.'
            )

            return Response(
                {
                    'message': message,
                    'added_quantity': quantity_to_add,
                    'existing_quantity': cart_item.quantity,
                    'cart_count': cart.items.count()
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

class BookSearchResultsAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        total_cart_items = count_cart_items(user)
        

        query = request.GET.get('search', '')
        books = []

        if query:
            books = Book.objects.filter(
                Q(book_name__icontains=query) |
                Q(author__icontains=query) |
                Q(genres__icontains=query)
            )

        context = {
            'books': books,
            'total_cart_items': total_cart_items,
            'search_query': query,
        }
        return render(request, 'bookorder/book_search_results.html', context)
        
  
class CartView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart).select_related('book', 'book__seller')

            cart_items_data = []
            total = 0

            for item in cart_items:
                item_total_price = item.book.book_price * item.quantity
                total += item_total_price

                # Total quantity of books uploaded by this seller
                seller_book_quantity = Book.objects.filter(
                    seller=item.book.seller,
                    book_name=item.book.book_name
                                ).aggregate(
                                    total_quantity=Sum('available_quantity')
                                )['total_quantity'] or 0


                cart_items_data.append({
                    'book': item.book,
                    'quantity': item.quantity,
                    'total_cart_price': item_total_price,
                    'seller_books_count': seller_book_quantity
                })

            total_cart_items = count_cart_items(user=request.user)

            return render(request, 'bookorder/cartview.html', {
                'cart_items': cart_items_data,
                'total': total,
                'total_cart_items': total_cart_items,
            })

        except Cart.DoesNotExist:
            return render(request, 'bookorder/cartview.html', {
                'cart_items': [],
                'total': 0,
                'total_cart_items': 0,
            })


class RemoveCartItemAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        cart = get_object_or_404(Cart, user=request.user)
        try:
            cart_item = cart.items.get(book_id=book_id)
            cart_item.delete()
            return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckoutAddressSerializer
from .models import CheckoutAddress

class CheckoutAPIView(APIView):
    def post(self, request):
        serializer = CheckoutAddressSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Checkout information saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
