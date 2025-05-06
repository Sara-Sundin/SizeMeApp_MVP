"""
Admin configuration for the CustomUser model.

This module defines a custom admin interface for the CustomUser model,
including how user fields are grouped and displayed in the Django admin.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.

    Organizes fields into logical sections including personal info,
    measurements, permissions, and important dates.
    """
    model = CustomUser

    list_display = [
        "email",
        "full_name",
        "avatar_number",
        "is_staff",
        "is_active",
    ]

    ordering = [
        "email",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "full_name",
                "avatar_number",
                "phone_number",
                "country",
                "postcode",
                "town_or_city",
                "street_address1",
                "street_address2",
                "county",
            )
        }),
        ("Measurements", {"fields": ("chest", "waist", "hips", "shoulders")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",
         "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "avatar_number",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "phone_number",
                "country",
                "postcode",
                "town_or_city",
                "street_address1",
                "street_address2",
                "county",
                "chest",
                "waist",
                "hips",
                "shoulders",
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
