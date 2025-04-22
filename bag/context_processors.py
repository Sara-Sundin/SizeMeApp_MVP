from home.models import Plan

def bag_contents(request):
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
            continue

    context = {
        'bag_items': bag_items,
        'total': total,
        'plan_count': plan_count,
    }
    return context
