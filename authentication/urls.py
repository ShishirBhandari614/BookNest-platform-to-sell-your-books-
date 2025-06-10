from django.urls import path
from .views import *

urlpatterns = [
    path('seller-signup/', SellerRegistrationView.as_view(), name='seller-registration'),
    path('buyer-signup/', BuyerRegistrationView.as_view(), name='buyer-registration'),
    path('seller-login/', SellerLoginView.as_view(), name='seller-login'),
    path('seller-logout/', SellerLogoutView.as_view(), name='seller-logout'),
    path('buyer-login/', BuyerLoginView.as_view(), name='buyer-login'),
    path('buyer-logout/', BuyerLogoutView.as_view(), name='buyer-logout'),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    # path('admin-logout/', AdminLogoutView.as_view(), name='admin-logout'),
  
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('check-username/', check_username, name='check-username'),
    path('check-email/', check_email, name='check-email'),
    path('check-phone/', check_phone, name='check-phone'),
    path('seller-dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
    path('buyer-dashboard/', BuyerDashboardView.as_view(), name='buyer-dashboard'),
]
