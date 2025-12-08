from django.db import models
from django.contrib.auth.models import  BaseUserManager ,AbstractBaseUser , PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField
class CustomManagerUser(BaseUserManager):
    """
    Manager for custom User model to handle user creation and superuser creation.
    """
    def create_user(self, phone_number , password=None , **extra_fields):
        """Create and return a regular user with phone_number."""
        if not phone_number:
            raise ValueError("User must provide phone number.")

        phone_number=phone_number.strip()

        user=self.model(
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self , phone_number , password , **extra_fields):

        """Create and return a Superuser with phone_number."""
        extra_fields.setdefault("is_superuser" , True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = CustomManagerUser()

    def __str__(self):
        return self.phone_number


