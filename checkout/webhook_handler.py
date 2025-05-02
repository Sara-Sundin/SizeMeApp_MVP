from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from accounts.models import CustomUser

import json
import time


class StripeWH_Handler:
    """
    Handle Stripe webhooks related to payment events.
    This includes creating orders after successful payment
    and sending confirmation emails to users.
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send a confirmation email to the customer after successful checkout.
        """
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        ).strip()
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            }
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    def handle_event(self, event):
        """
        Handle a generic, unknown, or unexpected webhook event.
        """
        print(f"Unhandled event type: {event['type']}")
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        This method:
        - Looks for an existing order matching the data.
        - If not found, creates a new order and line items.
        - Sends a confirmation email to the customer.
        """
        print("Webhook received: payment_intent.succeeded")

        intent = event.data.object
        pid = intent.id

        # Get metadata safely
        metadata = getattr(intent, "metadata", {})
        bag = getattr(metadata, "bag", "{}")
        save_info = getattr(metadata, "save_info", "off") == "on"
        username = getattr(metadata, "username", "AnonymousUser")

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Replace blank address fields with None
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Get user profile if authenticated
        profile = None
        if username != 'AnonymousUser':
            try:
                profile = CustomUser.objects.get(username=username)
                if save_info:
                    # Save delivery info to profile
                    profile.phone_number = shipping_details.phone
                    profile.country = shipping_details.address.country
                    profile.postcode = shipping_details.address.postal_code
                    profile.town_or_city = shipping_details.address.city
                    profile.street_address1 = shipping_details.address.line1
                    profile.street_address2 = shipping_details.address.line2
                    profile.county = shipping_details.address.state
                    profile.save()
            except CustomUser.DoesNotExist:
                print(f"User {username} not found")

        # Try to find existing matching order
        order_exists = False
        attempt = 1
        order = None
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            # Send email if order already exists
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already exists',
                status=200
            )
        else:
            try:
                # Create a new order
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )

                # Create line items for the order
                for item_id, item_data in json.loads(bag).items():
                    try:
                        product = Product.objects.get(id=item_id)
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    except Product.DoesNotExist:
                        print(f"Product with ID {item_id} not found")
            except Exception as e:
                if order:
                    order.delete()
                print(f"Error creating order: {e}")
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500
                )

        # Send confirmation email
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order created',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe.
        """
        print("Webhook received: payment_intent.payment_failed")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
