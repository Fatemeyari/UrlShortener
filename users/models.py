from django.db import models
from django.contrib.auth.models import  BaseUserManager

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




