from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PersonalSellerProfile, CorporateSellerProfile, BuyerProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number', 'full_name', 'is_seller', 'is_buyer', 'is_active', 'is_staff')
    list_filter = ('is_seller', 'is_buyer', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'full_name', 'phone_number')
   

class PersonalSellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'full_name')
    search_fields = ('user__email', 'user__username', 'full_name', 'phone_number')

class CorporateSellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'address', 'phone_number')
    search_fields = ('user__email', 'user__username', 'store_name', 'address', 'phone_number')

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number')
    search_fields = ('user__email', 'user__username', 'full_name', 'phone_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PersonalSellerProfile, PersonalSellerProfileAdmin)
admin.site.register(CorporateSellerProfile, CorporateSellerProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)