from decimal import Decimal
from django.test import TestCase
from checkout.models import Order, OrderLineItem
from home.models import Plan


class OrderSignalsTest(TestCase):

    def setUp(self):
        self.plan = Plan.objects.create(
            name="Signal Plan",
            plan_type="starter",
            monthly_price=10.00,
            setup_cost=50.00,
            short_description="Short",
            long_description="Long",
            features="One\nTwo"
        )

        self.order = Order.objects.create(
            full_name="Sara Skog",
            email="sara@example.com",
            phone_number="0701234567",
            country="SE",
            postcode="12345",
            town_or_city="Göteborg",
            street_address1="Storgatan 1",
            original_bag="{}",
            stripe_pid="abc123"
        )

    def test_order_total_updated_on_lineitem_create(self):
        self.assertEqual(self.order.order_total, Decimal("0"))
        OrderLineItem.objects.create(order=self.order, plan=self.plan, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("100.00"))

    def test_order_total_updated_on_lineitem_update(self):
        item = OrderLineItem.objects.create(order=self.order, plan=self.plan, quantity=1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("50.00"))

        item.quantity = 3
        item.save()  # triggers signal
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("150.00"))

    def test_order_total_updated_on_lineitem_delete(self):
        item = OrderLineItem.objects.create(order=self.order, plan=self.plan, quantity=2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("100.00"))

        item.delete()  # triggers signal
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("0.00"))
