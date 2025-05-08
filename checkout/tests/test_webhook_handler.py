import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from checkout.webhook_handler import StripeWH_Handler
from checkout.models import Order
from accounts.models import CustomUser
from products.models import Product, Category


class WebhookHandlerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="securepass123",
        )
        self.category = Category.objects.create(name="tshirts")
        self.product = Product.objects.create(
            name="Test Product",
            price=20.00,
            category=self.category
        )

    def simulate_event(self, type="payment_intent.succeeded"):
        intent_mock = MagicMock()
        intent_mock.id = "pi_12345"
        intent_mock.metadata = {
            "bag": json.dumps({str(self.product.id): 1}),
            "username": self.user.username,
            "save_info": "on"
        }
        charge_mock = MagicMock()
        charge_mock.billing_details.email = "test@example.com"
        charge_mock.amount = 2000
        intent_mock.charges.data = [charge_mock]

        shipping_address = MagicMock()
        shipping_address.country = "SE"
        shipping_address.postal_code = "12345"
        shipping_address.city = "Testville"
        shipping_address.line1 = "Street 1"
        shipping_address.line2 = ""
        shipping_address.state = "Region"

        shipping_mock = MagicMock()
        shipping_mock.name = "Test User"
        shipping_mock.phone = "1234567890"
        shipping_mock.address = shipping_address
        intent_mock.shipping = shipping_mock

        data_mock = MagicMock()
        data_mock.object = intent_mock

        event = MagicMock()
        event.type = type
        event.data = data_mock
        return event

    @patch("checkout.webhook_handler.StripeWH_Handler._send_confirmation_email")
    def test_handle_payment_intent_succeeded_creates_order(self, mock_send_email):
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = self.simulate_event()
        response = handler.handle_payment_intent_succeeded(event)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())
        mock_send_email.assert_called_once()

    def test_handle_event_unknown_type(self):
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = {"type": "unknown.event", "data": {}}
        response = handler.handle_event(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Unhandled webhook", response.content.decode())

    def test_handle_payment_intent_failed(self):
        request = self.factory.post('/webhook/')
        handler = StripeWH_Handler(request)
        event = {"type": "payment_intent.payment_failed", "data": {}}
        response = handler.handle_payment_intent_payment_failed(event)
        self.assertEqual(response.status_code, 200)
        self.assertIn("payment_intent.payment_failed", response.content.decode())
