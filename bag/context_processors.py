from home.models import Plan


def bag_contents(request):
    """
    Context processor that builds and returns bag contents for templates.

    Retrieves the current shopping bag from the session, looks up each
    Plan by ID, calculates subtotals, and returns a context dictionary
    containing:
        - bag_items: a list of plans with quantity and subtotal,
        - total: the full cost of all items in the bag,
        - plan_count: total number of plans in the bag.

    Returns:
        dict: Bag context to be used globally in templates.
    """
    bag_items = []
    total = 0
    plan_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        try:
            plan = Plan.objects.get(pk=int(item_id))
            subtotal = plan.setup_cost * quantity
            total += subtotal
            plan_count += quantity
            bag_items.append({
                'plan': plan,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Plan.DoesNotExist:
            continue  # Skip items that no longer exist

    context = {
        'bag_items': bag_items,
        'total': total,
        'plan_count': plan_count,
    }
    return context
