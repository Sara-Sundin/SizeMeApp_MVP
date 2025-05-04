from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    """
    Product admin using drag-and-drop sorting with adminsortable2.
    Note: Remove 'sort_order' from list_editable to enable drag handle.
    """
    list_display = ('name', 'category', 'price')  # Exclude sort_order to allow drag handle
    ordering = ('sort_order',)  # Sort by the custom field used for ordering


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Simple admin configuration for Category.
    """
    list_display = ('name', 'friendly_name')
