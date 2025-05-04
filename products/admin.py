from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import Product, Category
from sizemeapp.models import GarmentFit


class GarmentFitInline(admin.TabularInline):
    model = GarmentFit
    extra = 5
    fields = ('size_label', 'chest')


@admin.register(Product)
class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    """
    Product admin with drag-and-drop sort, GarmentFit inline,
    and image thumbnail in both list and detail view.
    """
    list_display = ('thumbnail', 'name', 'category', 'price')
    readonly_fields = ('image_preview',)
    ordering = ('sort_order',)
    inlines = [GarmentFitInline]

    # Fields shown in the product detail view
    fields = (
        'name', 'category', 'sku', 'description', 'has_sizes',
        'price', 'image', 'image_url', 'image_preview', 'sort_order'
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = "Preview"
