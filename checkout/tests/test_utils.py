from django.test import TestCase, override_settings
from django.core import mail
from django.conf import settings
from checkout.models import Order, OrderLineItem
from home.models import Plan
from checkout.utils import send_order_confirmation_email


@override_settings(DEFAULT_FROM_EMAIL='noreply@example.com')
class SendOrderEmailTest(TestCase):

    def setUp(self):
        self.plan = Plan.objects.create(
            name="Email Test Plan",
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

        OrderLineItem.objects.create(order=self.order, plan=self.plan, quantity=2)

    def test_send_order_confirmation_email_sends_email(self):
        send_order_confirmation_email(self.order)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertIn("Order", email.subject)
        self.assertIn("Sara Skog", email.body)
        self.assertEqual(email.to, [self.order.email])
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
