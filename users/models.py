"""Models for Users App."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Model definition for CustomUser."""

    username = models.CharField("Username", max_length=255, unique=True)
    email = models.EmailField("Email", max_length=255, unique=True, blank=True)
    first_name = models.CharField("First Name", max_length=255, blank=True)
    last_name = models.CharField("Last Name", max_length=255, blank=True)
    address = models.TextField("Address", blank=True)
    phone_number = models.CharField("Phone Number", max_length=15, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    is_staff = models.BooleanField("Is Staff", default=False)
    date_joined = models.DateTimeField("Date Joined", default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    # REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["username"]
        verbose_name = "custom user"
        verbose_name_plural = "custom users"
        app_label = "users"

    def __str__(self):
        return str(self.username)


