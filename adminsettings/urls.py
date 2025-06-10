from django.urls import path
from .views import *

urlpatterns = [
     path('custom-user-list/', CustomUserView.as_view(), name='custom-user-list'),
     path('buyer-list/', BuyerList.as_view(), name='buyer-list'),
     path('personal-seller-list/', PersonalSellerList.as_view(), name='seller-list'),
     path('corporate-seller-list/', CorporateSellerList.as_view(), name='corporate-seller-list'),
]
