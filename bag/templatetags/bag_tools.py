from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculates the subtotal for a given item based on its price and quantity.

    Args:
        price (Decimal or float): The unit price of the item.
        quantity (int): The number of units.

    Returns:
        Decimal or float: The total cost for the given quantity.
    """
    return price * quantity
