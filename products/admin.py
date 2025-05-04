from django.contrib import admin
from .models import Product, Category

# Register the Product model with custom admin configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model.
    Displays key fields in list view and adds search/filter functionality.
    """
    list_display = ('name', 'category', 'price')  # Fields shown in the product list view
    search_fields = ('name', 'description')       # Enables search by name and description
    list_filter = ('category',)                   # Adds a sidebar filter by category

# Register the Category model with basic admin configuration
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    Displays name and friendly name in the list view.
    """
    list_display = ('name', 'friendly_name')      # Fields shown in the category list view
