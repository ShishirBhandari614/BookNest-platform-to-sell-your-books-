# from re import A
from django.shortcuts import render
from authentication.models import CustomUser, BuyerProfile,PersonalSellerProfile,CorporateSellerProfile
from .decorators import admin_required
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponseForbidden, JsonResponse
from authentication.authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# def is_admin(user):
#     return user.is_authenticated and user.is_superuser


# @admin_required
class CustomUserView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        # print(user)
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        users = CustomUser.objects.all()
        return render(request, 'adminsettings/customuserlist.html', {'users': users})


class BuyerList(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        # print(user)
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        users = BuyerProfile.objects.all()
        return render(request, 'adminsettings/buyerlist.html', {'users': users})
        

class PersonalSellerList(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        # print(user)
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.")
        users = PersonalSellerProfile.objects.all()
        return render(request, 'adminsettings/sellerlist.html', {'users': users})
    
class CorporateSellerList(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # user = request.user
        # print(user)
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not authorized to access this page.") 
        users = CorporateSellerProfile.objects.all()
        return render(request, 'adminsettings/sellerlist.html', {'users': users})