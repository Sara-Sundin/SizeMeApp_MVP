from django.contrib import admin
from .models import GarmentFit
from products.models import Product


class GarmentFitInline(admin.TabularInline):
    """
    Inline admin configuration for GarmentFit.
    Allows adding and editing garment size data directly within the Product admin page.
    """
    model = GarmentFit
    extra = 5  # Display 5 empty rows for new entries
    fields = ('size_label', 'chest')  # Display only relevant fields in the inline
    # exclude = ('stretch_factor',)  # Optional: hide this field if unused in the admin


class ProductAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for Product model to include inline GarmentFit entries.
    """
    inlines = [GarmentFitInline]


# Unregister the default Product admin and register the customized version
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)


class GarmentFitAdmin(admin.ModelAdmin):
    """
    Admin configuration for standalone GarmentFit model (outside inline).
    Useful for searching, filtering, or managing all fits across products.
    """
    list_display = ('product', 'size_label', 'chest')  # Columns shown in list view
    list_filter = ('product',)  # Adds a filter sidebar by product


# Register GarmentFit model in the admin site
admin.site.register(GarmentFit, GarmentFitAdmin)
