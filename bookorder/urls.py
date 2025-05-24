from re import A
from django.urls import path
from .views import *
App_name = 'bookorder'
urlpatterns = [
    path('add-book/', AddBookView.as_view(), name='add_book'),
    path('list-book/', SellerBooksView.as_view(), name='list_book'),
    path('delete-book/<int:book_id>/', DeleteBookView.as_view(), name='delete-book'),
    path('edit-book/<int:pk>/', EditBookView.as_view(), name='edit-book'),
    path('buy-book/<int:pk>/', BuyBookView.as_view(), name='buy_book'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
] 


