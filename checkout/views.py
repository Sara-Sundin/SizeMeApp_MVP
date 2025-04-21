from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
import stripe

from .models import Plan
from checkout.models import Order, OrderLineItem
from .forms import OrderForm 

# Setup Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout_plan(request, plan_id):
    """
    Display checkout page for a single Plan and handle submission.
    """
    plan = get_object_or_404(Plan, pk=plan_id)

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = f'plan:{plan.id}'
            order.save()

            OrderLineItem.objects.create(
                order=order,
                plan=plan,
                quantity=1
            )

            return redirect(reverse('checkout_success', args=[order.order_number]))
    else:
        order_form = OrderForm()

    # Create Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=int(plan.setup_cost * 100),  # Stripe expects cents
        currency='usd',
    )

    context = {
        'plan': plan,
        'order_form': order_form,  # Pass form to template
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Display confirmation after successful checkout.
    """
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'checkout/checkout_success.html', {
        'order': order,
    })
