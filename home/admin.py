from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Plan model.
    Customizes how Plan instances are displayed and
    managed in the Django admin interface.
    """

    # Fields to display in the list view
    list_display = ('name', 'plan_type', 'monthly_price', 'setup_cost')

    # Enable search on name and short description fields
    search_fields = ('name', 'short_description')

    # Add filter sidebar for plan_type
    list_filter = ('plan_type',)

    # Organize fields into a fieldset in the admin detail form
    fieldsets = (
        (None, {
            'fields': (
                'name',  # Name of the plan
                'plan_type',  # Type (starter, growth, enterprise)
                'monthly_price',  # Monthly subscription price
                'setup_cost',  # One-time setup cost
                'short_description',  # Summary shown in previews
                'long_description',  # Detailed description
                'features',  # List of features (stored as JSON or list)
                'perfect_for',  # Target user group or use case
                'icon_class',  # Font Awesome icon class for display
                'button_class',  # CSS class for buttons
                'icon_color_class',  # CSS class for icon color
            )
        }),
    )
