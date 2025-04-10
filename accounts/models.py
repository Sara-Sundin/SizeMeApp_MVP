from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model using email for login, with full_name and measurement fields."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    chest = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hips = models.FloatField(blank=True, null=True)
    shoulders = models.FloatField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"] 

    def get_full_name(self):
        return self.full_name or self.email

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email

    def __str__(self):
        return self.get_short_name()
