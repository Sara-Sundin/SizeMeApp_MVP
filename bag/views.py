from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib import messages
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from home.models import Plan


def view_bag(request):
    """
    Display the contents of the shopping bag.

    Iterates over the session-stored bag, retrieves plan objects, calculates
    subtotals and total cost, and passes the data to the bag template.
    """
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0

    for plan_id_str, quantity in bag.items():
        try:
            plan = Plan.objects.get(pk=int(plan_id_str))
            subtotal = plan.setup_cost * quantity
            bag_items.append({
                'plan': plan,
                'quantity': quantity,
                'subtotal': subtotal,
                'item_id': plan_id_str,
            })
            total += subtotal
        except Plan.DoesNotExist:
            continue  # Skip if plan no longer exists

    context = {
        'bag_items': bag_items,
        'total': total,
        'grand_total': total,
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """
    Adds a plan to the bag.
    Replace the shopping bag with a single selected plan.
    Appends ?added=true to trigger the minicart.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    plan = get_object_or_404(Plan, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        return redirect('home')

    # Replace the bag with just this plan
    request.session['bag'] = {str(item_id): quantity}

    # Append or merge ?added=true to redirect URL
    redirect_url = request.POST.get('redirect_url', '/')
    parsed_url = urlparse(redirect_url)
    query_params = parse_qs(parsed_url.query)
    query_params['added'] = 'true'
    new_query = urlencode(query_params, doseq=True)
    updated_url = urlunparse(parsed_url._replace(query=new_query))

    return redirect(updated_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of a specific plan in the shopping bag.

    If quantity > 0: updates it.
    If quantity <= 0: removes the item.
    """
    plan = get_object_or_404(Plan, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity'))
    except (TypeError, ValueError):
        messages.error(request, 'Invalid quantity submitted.')
        return redirect(reverse('view_bag'))

    bag = request.session.get('bag', {})
    item_id_str = str(item_id)

    if quantity > 0:
        bag[item_id_str] = quantity
        messages.success
        (request, f'Updated {plan.name} quantity to {bag[item_id_str]}')
    else:
        bag.pop(item_id_str, None)
        messages.success(request, f'Removed {plan.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove a plan from the shopping bag completely.

    Returns HTTP 200 on success, 500 on failure.
    """
    plan = get_object_or_404(Plan, pk=item_id)

    try:
        bag = request.session.get('bag', {})
        bag.pop(str(item_id), None)
        request.session['bag'] = bag
        messages.success(request, f'Removed {plan.name} from your bag')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
