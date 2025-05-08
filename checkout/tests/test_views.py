from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from home.models import Plan
from checkout.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class CheckoutViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.plan = Plan.objects.create(
            name="Test Plan",
            plan_type="starter",
            monthly_price=10.00,
            setup_cost=50.00,
            short_description="Short",
            long_description="Long",
            features="One\nTwo"
        )
        self.session = self.client.session
        self.session['bag'] = {str(self.plan.id): 2}
        self.session.save()

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_get_view_renders_successfully(self, mock_stripe):
        mock_stripe.return_value.client_secret = 'test_secret'
        response = self.client.get(reverse('checkout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertIn('order_form', response.context)
        self.assertIn('client_secret', response.context)

    @patch('checkout.views.stripe.PaymentIntent.create')
    @patch('checkout.views.send_order_confirmation_email')
    def test_checkout_post_creates_order_and_redirects(self, mock_email, mock_stripe):
        mock_stripe.return_value.client_secret = 'test_secret'

        post_data = {
            'full_name': 'Sara Skog',
            'email': 'sara@example.com',
            'phone_number': '123456789',
            'country': 'SE',
            'postcode': '12345',
            'town_or_city': 'Göteborg',
            'street_address1': 'Main St 1',
            'street_address2': '',
            'county': 'Västra Götaland',
        }

        response = self.client.post(reverse('checkout'), post_data)
        order = Order.objects.first()

        self.assertRedirects(response, reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(order.email, 'sara@example.com')
        self.assertEqual(order.order_total, self.plan.setup_cost * 2)

    def test_checkout_redirects_if_bag_is_empty(self):
        session = self.client.session
        session['bag'] = {}  # Empty the bag
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse('view_bag'))

    @patch('checkout.views.send_order_confirmation_email')
    def test_checkout_success_view(self, mock_email):
        order = Order.objects.create(
            full_name='Sara Skog',
            email='sara@example.com',
            phone_number='0701234567',
            country='SE',
            postcode='12345',
            town_or_city='Göteborg',
            street_address1='Main St 1',
            original_bag='{}',
            stripe_pid='abc123'
        )

        # Set the session flag required by the view
        session = self.client.session
        session['just_ordered'] = True
        session.save()

        url = reverse('checkout_success', args=[order.order_number])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertEqual(response.context['order'], order)
        mock_email.assert_called_once_with(order)
