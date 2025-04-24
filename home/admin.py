from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'monthly_price', 'setup_cost')
    search_fields = ('name', 'short_description')
    list_filter = ('plan_type',)
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'plan_type',
                'monthly_price',
                'setup_cost',
                'short_description',
                'long_description',
                'features',
                'perfect_for',
                'icon_class', 
                'button_class',
                'icon_color_class',
            )
        }),
    )
