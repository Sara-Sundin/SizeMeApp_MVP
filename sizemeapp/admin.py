from django.contrib import admin
from .models import GarmentFit


@admin.register(GarmentFit)
class GarmentFitAdmin(admin.ModelAdmin):
    list_display = ('product', 'size_label', 'chest')
    list_filter = ('product',)
