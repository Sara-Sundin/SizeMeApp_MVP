from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json
import stripe


class WebhookViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("webhook")
        self.payload = json.dumps({"id": "evt_test_webhook", "object": "event"})
        self.sig_header = "t=12345,v1=fake_signature"

    @patch("stripe.Webhook.construct_event")
    def test_valid_payment_intent_event(self, mock_construct_event):
        mock_construct_event.return_value = {
            "type": "payment_intent.payment_failed"
        }
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )
        self.assertEqual(response.status_code, 200)

    @patch("stripe.Webhook.construct_event", side_effect=ValueError("Invalid payload"))
    def test_invalid_payload_returns_400(self, _):
        response = self.client.post(
            self.url,
            data="not-json",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )
        self.assertEqual(response.status_code, 400)

    @patch("stripe.Webhook.construct_event", side_effect=stripe.error.SignatureVerificationError("bad sig", "sig"))
    def test_invalid_signature_returns_400(self, _):
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )
        self.assertEqual(response.status_code, 400)

    @patch("stripe.Webhook.construct_event", side_effect=Exception("unexpected error"))
    def test_generic_exception_returns_400(self, _):
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=self.sig_header,
        )
        self.assertEqual(response.status_code, 400)
