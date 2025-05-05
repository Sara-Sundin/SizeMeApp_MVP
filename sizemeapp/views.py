from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from products.models import Product
from .utils.recommendations import get_size_recommendations


def size_recommendation_view(request, product_id):
    """
    Returns size recommendations for a given product
    and authenticated user as JSON.

    Expected to be used in AJAX calls or API requests.

    Args:
        request: HTTP request object.
        product_id: ID of the product to get size recommendations for.

    Returns:
        JsonResponse: A dictionary with the list of recommended sizes.
    """
    product = get_object_or_404(Product, pk=product_id)
    recommendations = []

    # Ensure user is logged in and has a chest measurement stored
    if (
        request.user.is_authenticated
        and hasattr(request.user, 'chest')
        and request.user.chest
    ):
        user_chest = request.user.chest
        recommendations = get_size_recommendations(user_chest, product)

    return JsonResponse({'recommendations': recommendations})


def toggle_size_mode(request):
    """
    Toggles the session-based 'size_mode' on or off.
    Sets a flag for frontend to display a confirmation modal.

    This allows users to enter or exit 'size-aware browsing mode',
    where size recommendations are shown based on body measurements.

    Returns:
        Redirect to the referring page or 'webshop' if not found.
    """
    current_mode = request.session.get('size_mode', False)

    # Toggle mode
    request.session['size_mode'] = not current_mode

    # Set flags used to trigger modals on the frontend
    if request.session['size_mode']:
        request.session['size_mode_entered'] = True
    else:
        request.session['size_mode_exited'] = True

    return redirect(request.META.get('HTTP_REFERER', 'webshop'))
