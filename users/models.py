from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, username = username, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    # name = models.CharField(max_length=25)
    password = models.CharField(max_length=100)  # Already handled by Django
    location = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)  # ✅ Use is_active (Django standard)
    is_staff = models.BooleanField(default=False)  # ✅ Use is_staff (Django standard)
    is_superuser = models.BooleanField(default=False)  # ✅ Use is_superuser (Django standard)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = "email"  # Login using email instead of username
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()  # Ensure Django uses CustomUserManager

    def __str__(self):
        return self.email
