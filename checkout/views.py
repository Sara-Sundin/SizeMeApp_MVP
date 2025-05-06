from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
import stripe

from home.models import Plan
from checkout.models import Order, OrderLineItem
from .forms import OrderForm
from .utils import send_order_confirmation_email
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import login_required

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


def checkout(request):
    """
    Handle the checkout process:
    - Display order summary
    - Validate and save form data
    - Create Stripe intent and order/line items
    - Save delivery info
    - Redirect to success page
    """
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
        save_info = request.POST.get('save_info') == 'on'

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = str(bag)

            # Link user to the order if logged in
            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item in bag_items:
                OrderLineItem.objects.create(
                    order=order,
                    plan=item['plan'],
                    quantity=item['quantity']
                )

            if request.user.is_authenticated and save_info:
                user = request.user
                user.full_name = order.full_name
                user.phone_number = order.phone_number
                user.country = order.country
                user.postcode = order.postcode
                user.town_or_city = order.town_or_city
                user.street_address1 = order.street_address1
                user.street_address2 = order.street_address2
                user.county = order.county
                user.save()

            request.session['bag'] = {}

            # Set session flag for secure success access
            request.session['just_ordered'] = True

            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. "
                "Please check your information."
            )
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
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

    else:
        if request.user.is_authenticated:
            user = request.user
            initial_data = {
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'country': user.country,
                'postcode': user.postcode,
                'town_or_city': user.town_or_city,
                'street_address1': user.street_address1,
                'street_address2': user.street_address2,
                'county': user.county,
            }
            order_form = OrderForm(initial=initial_data)
        else:
            order_form = OrderForm()

        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
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
    Secure successful checkout:
    - Allow access only right after an order (via session flag)
    - If authenticated, make sure user owns the order
    - Clear session flag to prevent reuse
    """
    order = get_object_or_404(Order, order_number=order_number)

    session_flag = request.session.get('just_ordered')

    # Only allow if session flag exists (order just placed)
    if not session_flag:
        return HttpResponseForbidden("You cannot access this page directly.")

    # If user is authenticated, make sure it's their order
    if (
        request.user.is_authenticated
        and order.user
        and order.user != request.user
    ):
        return HttpResponseForbidden
        ("You do not have permission to view this order.")

    # Clean up session
    request.session.pop('just_ordered', None)

    send_order_confirmation_email(order)
    messages.success(
        request,
        f"Order successfully processed! "
        f"Your order number is {order.order_number}."
    )
    return render(request, 'checkout/checkout_success.html', {'order': order})


@login_required
def order_history(request):
    """
    Show all orders placed by the logged-in user
    """
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'checkout/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    """
    View details of a past order from order history.
    Only the user who placed the order can view it.
    """
    order = get_object_or_404(Order, order_number=order_number)

    if order.user != request.user:
        return HttpResponseForbidden
        ("You do not have permission to view this order.")

    return render(request, 'checkout/order_detail.html', {'order': order})
