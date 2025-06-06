import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from home.models import Plan


class Order(models.Model):
    """
    A model to store all order-related information.

    Includes customer info, shipping address, payment metadata,
    and auto-generated order number. Related line items are tracked
    via a reverse relationship through the 'lineitems' related_name.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    # Order metadata
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=''
    )

    def _generate_order_number(self):
        """
        Generate a unique, 8-character uppercase order number
        """
        while True:
            order_number = uuid.uuid4().hex[:8].upper()
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def update_total(self):
        """
        Calculate and update the order totals by aggregating the sum
        of all related line items' totals. No delivery cost is applied.
        """
        self.order_total = (
            self.lineitems.aggregate(Sum('lineitem_total'))[
                'lineitem_total__sum'
            ] or 0
        )
        self.delivery_cost = 0  # No delivery for digital plans
        self.grand_total = self.order_total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override default save method to assign an order number
        if one hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Individual line item within an order.
    Links to a Plan and tracks quantity and subtotal.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems',
    )
    plan = models.ForeignKey(
        Plan, null=True, blank=True, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=1)
    lineitem_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False,
    )

    def save(self, *args, **kwargs):
        """
        Override default save method to set line item total based
        on the setup cost of the associated plan and its quantity.
        """
        if self.plan:
            self.lineitem_total = self.plan.setup_cost * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'Plan {self.plan.name} on order {self.order.order_number}'
            if self.plan else f'Item on {self.order.order_number}'
        )
