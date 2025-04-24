from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
import stripe

from home.models import Plan
from checkout.models import Order, OrderLineItem
from .forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


def checkout(request):
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
        print("POST request received. Save info:", save_info)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.original_bag = str(bag)
            order.save()
            print("Order saved:", order)

            for item in bag_items:
                OrderLineItem.objects.create(
                    order=order,
                    plan=item['plan'],
                    quantity=item['quantity']
                )
            print("Order line items saved.")

            if request.user.is_authenticated and save_info:
                print("✅ User is authenticated and chose to save info")

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

                print(f"✅ Saved user profile: {user}")
            else:
                print("⚠️ Save block not triggered. Authenticated:", request.user.is_authenticated, "| Save Info:", save_info)

            request.session['bag'] = {}
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please check your information.")
            print("Form errors:", order_form.errors)

            # Create a new PaymentIntent if form is invalid
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
            print("Prefilling form with user data:", initial_data)
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
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f"Order successfully processed! Your order number is {order.order_number}.")
    return render(request, 'checkout/checkout_success.html', {'order': order})
