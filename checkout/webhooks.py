import stripe
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    """
    Listen for webhooks from Stripe, verify their signature,
    and delegate the handling to appropriate methods.
    """
    # --- Setup Stripe ---
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # --- Retrieve and verify the webhook payload and signature ---
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    except Exception as e:
        # Any other unexpected error
        return HttpResponse(content=e, status=400)

    # --- Initialize custom webhook handler ---
    handler = StripeWH_Handler(request)

    # --- Map Stripe event types to handler methods ---
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # --- Identify the type of event ---
    event_type = event['type']

    # --- Get the appropriate handler function (or default to generic) ---
    event_handler = event_map.get(event_type, handler.handle_event)

    # --- Call the handler and return the response ---
    response = event_handler(event)
    return response
