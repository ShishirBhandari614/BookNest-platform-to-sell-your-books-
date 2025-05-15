from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SellerProfile, BuyerProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'full_name', 'is_seller', 'is_buyer', 'is_active', 'is_staff')
    list_filter = ('is_seller', 'is_buyer', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name', 'phone_number')
   

class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'full_name', 'address')
    search_fields = ('user__email', 'user__username', 'full_name', 'phone_number', 'address')

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number')
    search_fields = ('user__email', 'user__username', 'full_name', 'phone_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SellerProfile, SellerProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)