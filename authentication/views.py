from django.shortcuts import render,redirect
from rest_framework.views import APIView
from . serializer import *
from rest_framework.response import Response,SimpleTemplateResponse
from rest_framework import status
from bookorder.models import Book
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import os
from authentication.authentication import CookieJWTAuthentication
from bookorder.models import CartItem
# Create your views here.
class SellerRegistrationView(APIView):
    def get(self, request):
        serializer = SellerSignupSerializer()
        return SimpleTemplateResponse('authentication/signup.html', {'serializer': serializer})

    def post(self, request):
        try:
            serializer = SellerSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Signup successful',
                    'status': 'success'
                }, status=status.HTTP_201_CREATED)
            else:
                # Format validation errors for frontend
                error_messages = {}
                for field, errors in serializer.errors.items():
                    if isinstance(errors, list):
                        error_messages[field] = errors[0]
                    else:
                        error_messages[field] = str(errors)
                
                return Response({
                    'status': 'error',
                    'errors': error_messages
                }, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({
                'status': 'error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'errors': {'general': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
class BuyerRegistrationView(APIView):
    def get(self, request):
        serializer = BuyerSignupSerializer()
        return SimpleTemplateResponse('authentication/buyer_signup.html', {'serializer': serializer})

    def post(self, request):
        try:
            serializer = BuyerSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Signup successful',
                    'status': 'success'
                }, status=status.HTTP_201_CREATED)
            else:
                # Format validation errors for frontend
                error_messages = {}
                for field, errors in serializer.errors.items():
                    if isinstance(errors, list):
                        error_messages[field] = errors[0]
                    else:
                        error_messages[field] = str(errors)
                
                return Response({
                    'status': 'error',
                    'errors': error_messages
                }, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({
                'status': 'error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': 'error',
                'errors': {'general': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)
            
            

# class SellerLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(email=email, password=password)

#         if user and user.is_seller:  # Ensure the user is a seller
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }, status=status.HTTP_200_OK)

#         return Response({'error': 'Invalid credentials or not a seller'}, status=status.HTTP_401_UNAUTHORIZED)


class SellerLoginView(APIView):
    def get(self, request):
        serializer = SellerLoginSerializer()
        return SimpleTemplateResponse('authentication/seller_login.html', {'serializer': serializer})

    def post(self, request):
        serializer = SellerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_seller:
                return Response({'detail': 'Access denied. User is not a seller.'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            # Set the JWT in a cookie
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,  # Prevent JavaScript access to the cookie
                secure=os.getenv('DJANGO_ENV') == 'production',  # Use secure cookies in production
                samesite='Lax'  # Adjust based on your cross-site requirements
            )
            return response
        else:
            if not CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# View for User Logout (Blacklisting Refresh Token)
class SellerLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SellerLogoutSerializer(data=request.data)

        if serializer.is_valid():
            # ✅ Get the refresh token after checking serializer validity
            refresh_token = serializer.validated_data.get("refresh")  

            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyerLoginView(APIView):
    def get(self, request):
        serializer = BuyerLoginSerializer()
        return SimpleTemplateResponse('authentication/buyer_login.html', {'serializer': serializer})

    def post(self, request):
        serializer = BuyerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_buyer:
                return Response({'detail': 'Access denied. User is not a seller.'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            # Set the JWT in a cookie
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,  # Prevent JavaScript access to the cookie
                secure=os.getenv('DJANGO_ENV') == 'production',  # Use secure cookies in production
                samesite='Lax'  # Adjust based on your cross-site requirements
            )
            return response
        else:
            if not CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminLoginView(APIView):
    def get(self, request):
        serializer = adminloginSerializer()
        return SimpleTemplateResponse('authentication/adminlogin.html', {'serializer': serializer})

    def post(self, request):
        serializer = adminloginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_superuser:
                return Response({'detail': 'Access denied. User is not an admin.'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            # Set the JWT in a cookie
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,  # Prevent JavaScript access to the cookie
                secure=os.getenv('DJANGO_ENV') == 'production',  # Use secure cookies in production
                samesite='Lax'  # Adjust based on your cross-site requirements
            )
            return response
        else:
            if not CustomUser.objects.filter(email=email).exists():
                return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
           
class BuyerLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BuyerLogoutSerializer(data=request.data)

        if serializer.is_valid():
            # ✅ Get the refresh token after checking serializer validity
            refresh_token = serializer.validated_data.get("refresh")  

            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["POST"])
def check_username(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        exists = CustomUser.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def check_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        exists = CustomUser.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
class SellerDashboardView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_seller:
            print("User is not a seller")
            return Response({'detail': 'Access denied. User is not a seller.'}, status=status.HTTP_403_FORBIDDEN)

        return render(request, 'authentication/seller_dashboard.html')


def count_cart_items():
    return CartItem.objects.count()
class BuyerDashboardView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_cart_items = count_cart_items()

        user = request.user

        if not user.is_buyer:
            print("User is not a buyer")
            return Response({'detail': 'Access denied. User is not a buyer.'}, status=status.HTTP_403_FORBIDDEN)

        books = Book.objects.all().order_by('?')[:12]  # Random 12 books
        return render(request, 'authentication/buyer_dashboard.html', {'books': books, 'total_cart_items': total_cart_items})


class AdminDashboardView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_superuser:
            print("User is not an admin")
            return Response({'detail': 'Access denied. User is not an admin.'}, status=status.HTTP_403_FORBIDDEN)

        return render(request, 'authentication/admindas.html')