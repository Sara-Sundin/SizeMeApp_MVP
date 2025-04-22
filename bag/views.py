from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib import messages

from home.models import Plan


def view_bag(request):
    """A view that renders the bag contents page with plan data."""
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
            continue

    context = {
        'bag_items': bag_items,
        'total': total,
        'grand_total': total,  # No delivery cost
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_id):
    """Add a quantity of the specified plan to the shopping bag."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    plan = get_object_or_404(Plan, pk=item_id)

    try:
        quantity = int(request.POST.get('quantity'))
    except (TypeError, ValueError):
        messages.error(request, 'Invalid quantity submitted.')
        return redirect('home')

    redirect_url = request.POST.get('redirect_url', '/')
    bag = request.session.get('bag', {})
    item_id_str = str(item_id)

    if item_id_str in bag:
        bag[item_id_str] += quantity
        messages.success(request, f'Updated {plan.name} quantity to {bag[item_id_str]}')
    else:
        bag[item_id_str] = quantity
        messages.success(request, f'Added {plan.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified plan."""
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
        messages.success(request, f'Updated {plan.name} quantity to {bag[item_id_str]}')
    else:
        bag.pop(item_id_str, None)
        messages.success(request, f'Removed {plan.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the plan from the shopping bag."""
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
