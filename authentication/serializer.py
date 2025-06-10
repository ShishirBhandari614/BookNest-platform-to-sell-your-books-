from rest_framework import serializers
from .models import CustomUser, SellerProfile, PersonalSellerProfile, CorporateSellerProfile, BuyerProfile
from django.db import transaction
from rest_framework.authtoken.models import Token

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number','full_name', 'is_seller', 'is_buyer']

class PersonalSellerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'full_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        full_name = validated_data.pop('full_name')
        phone_number = validated_data.pop('phone_number')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            is_seller=True
        )
        # Create the base SellerProfile
        PersonalSellerProfile.objects.create(
            user=user,
            seller_type='personal',
            full_name=full_name,
            phone_number=phone_number
        )
        return user

class CorporateSellerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    store_name = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [ 'email', 'phone_number', 'store_name', 'address', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if not data.get('store_name') or not data.get('address'):
            raise serializers.ValidationError("Corporate sellers must provide store name and address.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        store_name = validated_data.pop('store_name')
        address = validated_data.pop('address')
        phone_number = validated_data.pop('phone_number')
        email = validated_data['email']
        username = email
        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            full_name=store_name,  # or use a separate field if you want
            password=password,
            is_seller=True
        )
        # Create the base SellerProfile
        
        
        # Create the corporate sub-profile
        CorporateSellerProfile.objects.create(
            user=user,
            seller_type='corporate',
            store_name=store_name,
            address=address,
            phone_number=phone_number
        )
        return user

class BuyerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    full_name = serializers.CharField(max_length=255)
    # shipping_address = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number','full_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def validate(self, data):
        
    #     # Check for duplicate username
    #     if CustomUser.objects.filter(username=data['username']).exists():
    #         raise serializers.ValidationError({
    #             'username': 'This username is already taken. Please choose another one.'
    #         })
        
    #     # Check for duplicate email
    #     if CustomUser.objects.filter(email=data['email']).exists():
    #         raise serializers.ValidationError({
    #             'email': 'This email is already registered. Please use another email or login.'
    #         })
        
    #     return data

    def save(self, **kwargs):
        try:
            # Validate and create the user
            user = CustomUser(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
                phone_number=self.validated_data['phone_number']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            
            # Check if passwords match
            if password != password2:
                raise serializers.ValidationError({'error': 'Passwords do not match'})
            
            user.set_password(password)
            user.is_buyer = True
            user.save()

            # Create the buyer profile
            BuyerProfile.objects.create(
                user=user,
                full_name=self.validated_data['full_name'],
                phone_number=self.validated_data['phone_number'],
                # shipping_address=self.validated_data['shipping_address']
            )
            
            return user
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})


class SellerLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
class BuyerLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class adminloginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
class SellerLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
class BuyerLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()