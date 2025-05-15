from django.urls import path
from .views import *

urlpatterns = [
     path('custom-user-list/', CustomUserView.as_view(), name='custom-user-list'),
     path('buyer-list/', BuyerList.as_view(), name='buyer-list'),
     path('seller-list/', SellerList.as_view(), name='seller-list'),
]
