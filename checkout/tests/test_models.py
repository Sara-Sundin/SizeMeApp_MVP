from decimal import Decimal
from django.test import TestCase
from checkout.models import Order, OrderLineItem
from home.models import Plan
from django.contrib.auth import get_user_model


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
        email="testuser@example.com",
        username="testuser@example.com",  # Set username equal to email
        password="testpass123"
    )

        self.plan = Plan.objects.create(
            name="Test Plan",
            plan_type="starter",
            monthly_price=29.99,
            setup_cost=100.00,
            short_description="Short",
            long_description="Long description",
            features="Feature 1\nFeature 2"
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name="Sara Skog",
            email="sara@example.com",
            phone_number="0701234567",
            country="SE",
            postcode="41101",
            town_or_city="Gothenburg",
            street_address1="Main St 1",
            street_address2="",
            county="Västra Götaland",
            original_bag="{}",
            stripe_pid="test_pid"
        )

    def test_order_number_is_generated(self):
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(len(self.order.order_number), 32)

    def test_update_total_calculates_correctly(self):
        OrderLineItem.objects.create(
            order=self.order,
            plan=self.plan,
            quantity=2
        )
        self.order.update_total()
        self.assertEqual(self.order.order_total, Decimal('200.00'))
        self.assertEqual(self.order.grand_total, Decimal('200.00'))

    def test_order_str_returns_order_number(self):
        self.assertEqual(str(self.order), self.order.order_number)


class OrderLineItemModelTest(TestCase):

    def setUp(self):
        self.plan = Plan.objects.create(
            name="Basic Plan",
            plan_type="starter",
            monthly_price=19.99,
            setup_cost=50.00,
            short_description="A plan",
            long_description="Details here",
            features="Feature A"
        )
        self.order = Order.objects.create(
            full_name="Alex Doe",
            email="alex@example.com",
            phone_number="0712345678",
            country="SE",
            postcode="12345",
            town_or_city="Uppsala",
            street_address1="Testgatan 2",
            county="Uppland",
            original_bag="{}",
            stripe_pid="pid_abc"
        )

    def test_lineitem_total_is_computed_on_save(self):
        item = OrderLineItem.objects.create(
            order=self.order,
            plan=self.plan,
            quantity=3
        )
        self.assertEqual(item.lineitem_total, Decimal('150.00'))

    def test_str_representation_with_plan(self):
        item = OrderLineItem.objects.create(
            order=self.order,
            plan=self.plan,
            quantity=1
        )
        self.assertIn(self.plan.name, str(item))
        self.assertIn(self.order.order_number, str(item))

    def test_str_representation_without_plan(self):
        item = OrderLineItem.objects.create(
        order=self.order,
        plan=None,
        quantity=1,
        lineitem_total=0 
)

        self.assertIn(self.order.order_number, str(item))
        self.assertIn("Item on", str(item))
