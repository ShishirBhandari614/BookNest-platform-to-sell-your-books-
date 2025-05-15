from rest_framework import serializers
from .models import CustomUser, SellerProfile, BuyerProfile
from django.db import transaction
from rest_framework.authtoken.models import Token

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number','full_name', 'is_seller', 'is_buyer']

class SellerSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    address = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'full_name', 'address', 'password', 'password2']
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
            user = CustomUser(
                username=self.validated_data['username'],
                email=self.validated_data['email'],
                phone_number=self.validated_data['phone_number'],
                full_name=self.validated_data['full_name']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']
            
            if password != password2:
                raise serializers.ValidationError({'error': 'Passwords do not match'})
            
            user.set_password(password)
            user.is_seller = True
            user.save()

            # Create the seller profile with full_name
            SellerProfile.objects.create(
                user=user,
                phone_number=self.validated_data['phone_number'],
                full_name=self.validated_data['full_name'],
                address=self.validated_data['address']
            )
            
            return user
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})

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