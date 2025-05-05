from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Inline admin class to allow editing of order line items directly
    within the Order admin interface.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Order model.
    Displays and manages orders along with their related line items.
    """
    inlines = (OrderLineItemAdminInline,)

    # Fields that are read-only in the admin form
    readonly_fields = (
        'order_number', 'date',
        'delivery_cost', 'order_total',
        'grand_total', 'original_bag',
        'stripe_pid',
    )

    # Fields shown in the admin form
    fields = (
        'order_number', 'user_profile', 'date', 'full_name',
        'email', 'phone_number', 'country',
        'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county', 'delivery_cost',
        'order_total', 'grand_total', 'original_bag',
        'stripe_pid',
    )

    # Columns displayed in the list view
    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost',
        'grand_total',
    )

    # Default ordering for the list view
    ordering = ('-date',)


# Register the Order model with its custom admin interface
admin.site.register(Order, OrderAdmin)
