from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer
from .models import Book
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