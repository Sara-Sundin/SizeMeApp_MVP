from django.contrib import admin
from .models import GarmentFit
from products.models import Product


# Inline admin to add GarmentFit directly in the Product admin
class GarmentFitInline(admin.TabularInline):
    model = GarmentFit
    extra = 5  # Number of empty rows shown for adding sizes
    fields = ('size_label', 'chest')  # Only show relevant fields
    # exclude = ('stretch_factor',)  # Uncomment if you want to hide stretch_factor


# Custom Product admin with inline
class ProductAdmin(admin.ModelAdmin):
    inlines = [GarmentFitInline]


admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)


class GarmentFitAdmin(admin.ModelAdmin):
    list_display = ('product', 'size_label', 'chest')
    list_filter = ('product',)

