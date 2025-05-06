from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that uses email instead of username for authentication.

    Includes additional fields for full name, body measurements (chest, waist,
    hips, shoulders), and contact/address details (phone number, country, city,
    etc.).
    """

    # Authentication
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    # Avatar
    avatar_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Selected avatar image number"
    )

    # Measurement fields (optional, used for size recommendations)
    chest = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hips = models.FloatField(blank=True, null=True)
    shoulders = models.FloatField(blank=True, null=True)

    # Contact and address fields (all optional)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, blank=True, null=True)
    street_address1 = models.CharField(max_length=80, blank=True, null=True)
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    county = models.CharField(max_length=80, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_full_name(self):
        """Return the user's full name or fallback to email if not set."""
        return self.full_name or self.email

    def get_short_name(self):
        """Return the first part of the user's full name or
        email if not set."""
        return self.full_name.split()[0] if self.full_name else self.email

    def __str__(self):
        """String representation of the user (short name or email)."""
        return self.get_short_name()
