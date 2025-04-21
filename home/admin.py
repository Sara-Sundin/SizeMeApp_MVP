from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'monthly_price', 'setup_cost', 'order')
    list_editable = ('order',)
    ordering = ('order',)
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
            )
        }),
        ('Visual & CTA Settings', {
            'fields': (
                'icon_class',
                'cta_label',
                'contact_cta_label',
                'order',
            ),
            'classes': ('collapse',),
        }),
    )
