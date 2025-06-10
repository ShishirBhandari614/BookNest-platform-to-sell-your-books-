from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, full_name, password=None, is_seller=False, is_buyer=False):
        """Creates and returns a user with the given email and password."""
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, full_name=full_name, is_seller=is_seller, is_buyer=is_buyer)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_seller(self, email, username, password=None):
        """Creates and returns a seller."""
        return self.create_user(email, username, password, is_seller=True, is_buyer=False)

    def create_buyer(self, email, username, password=None):
        """Creates and returns a buyer."""
        return self.create_user(email, username, password, is_buyer=True, is_seller=False)

    def create_superuser(self, email, username, password=None, phone_number='', full_name='Admin'):
        """Creates and returns a superuser."""
        user = self.create_user(
            email=email,
            username=username,
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            is_seller=False,
            is_buyer=False
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15)
    full_name = models.CharField(max_length=255)  # Added full_name field
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Now requires a username

    def __str__(self):
        return self.email

# Seller Profile Model
class SellerProfile(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='seller_profile')
    seller_type = models.CharField(max_length=10, choices=[('personal', 'Personal'), ('corporate', 'Corporate')])
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # Add any fields common to all sellers here

    class Meta:
        verbose_name = 'Seller Profile'
        verbose_name_plural = 'Seller Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.seller_type})"

class PersonalSellerProfile(SellerProfile):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    # Add any other personal-specific fields

    class Meta:
        verbose_name = 'Personal Seller Profile'
        verbose_name_plural = 'Personal Seller Profiles'

    def __str__(self):
        return f"{self.full_name} (Personal Seller)"

class CorporateSellerProfile(SellerProfile):
    store_name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    # Add any other corporate-specific fields

    class Meta:
        verbose_name = 'Corporate Seller Profile'
        verbose_name_plural = 'Corporate Seller Profiles'

    def __str__(self):
        return f"{self.store_name} (Corporate Seller)"

# Buyer Profile Model
class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="buyer_profile")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    # shipping_address = models.TextField()

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"
