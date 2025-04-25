# sizemeapp/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from products.models import Product
from .utils.recommendations import get_size_recommendations
from django.shortcuts import redirect


def size_recommendation_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    recommendations = []

    if request.user.is_authenticated and hasattr(request.user, 'chest') and request.user.chest:
        user_chest = request.user.chest
        recommendations = get_size_recommendations(user_chest, product)

    return JsonResponse({'recommendations': recommendations})


def toggle_size_mode(request):
    current_mode = request.session.get('size_mode', False)
    request.session['size_mode'] = not current_mode

    # Set a flag to trigger a success modal message
    if request.session['size_mode']:
        request.session['size_mode_entered'] = True
    else:
        request.session['size_mode_exited'] = True

    return redirect(request.META.get('HTTP_REFERER', 'webshop'))
