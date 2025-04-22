from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
import stripe

from home.models import Plan
from checkout.models import Order, OrderLineItem
from .forms import OrderForm

# Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """ Handle checkout for all plans in the session bag """

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect('view_bag')

    bag_items = []
    total = 0

    for plan_id, quantity in bag.items():
        plan = get_object_or_404(Plan, pk=int(plan_id))
        subtotal = plan.setup_cost * quantity
        total += subtotal
        bag_items.append({
            'plan': plan,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = str(bag)
            order.save()

            for item in bag_items:
                OrderLineItem.objects.create(
                    order=order,
                    plan=item['plan'],
                    quantity=item['quantity']
                )

            # Clear bag after successful order
            request.session['bag'] = {}

            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please check your info.")
    else:
        order_form = OrderForm()

    # Stripe PaymentIntent
    intent = stripe.PaymentIntent.create(
        amount=int(total * 100),  # Stripe uses cents
        currency='usd',
    )

    context = {
        'order_form': order_form,
        'bag_items': bag_items,
        'total': total,
        'grand_total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, f'Order successfully processed! Your order number is {order.order_number}.')
    return render(request, 'checkout/checkout_success.html', {'order': order})
