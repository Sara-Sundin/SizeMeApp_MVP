from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Customizing the Django Admin interface for the CustomUser model
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    # Defines the columns displayed in the admin user list
    list_display = ["email", "full_name", "is_staff", "is_active"]
    ordering = ["email"]  # Orders users by email

    # Fields to display when viewing/editing a user in the admin panel
    fieldsets = (
         (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name",)}),
        ("Measurements", {"fields": ("chest", "waist", "hips", "shoulders")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields to display when adding a new user in the admin panel
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "password1",
                "is_staff",
                "is_active"
            ),
        }),
    )


# Register the CustomUser model with the Django admin site
admin.site.register(CustomUser, CustomUserAdmin)