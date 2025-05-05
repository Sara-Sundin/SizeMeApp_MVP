from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import MeasurementUpdateForm
from products.models import Product
from sizemeapp.utils.recommendations import get_size_recommendations

# Import or define this dict if it's not global
CATEGORY_BUTTON_CLASSES = {
    'tshirts': 'cta-btn--primary',
    'shirts': 'cta-btn--tertiary',
    'sweatshirts': 'cta-btn--black',
}


def webshop_view(request):
    """
    Render the main webshop landing page.

    If 'size_mode' is not already set in the user's session,
    it will default to True. This is used to enable size-related
    features in the frontend.
    """
    if 'size_mode' not in request.session:
        request.session['size_mode'] = True
    return render(request, 'webshop/webshop.html')


@login_required
def update_measurements_from_webshop(request):
    """
    Handle measurement update submission from the modal
    in the product detail view.
    Validates using Django form. If invalid, re-renders
    the product page with error messages.
    """
    if request.method == 'POST':
        form = MeasurementUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.session['show_webshop_measurements_success'] = True
            return redirect(request.META.get('HTTP_REFERER', 'products'))

        # Fallback: get product_id from hidden input
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        size_mode = request.session.get('size_mode', False)
        recommendations = []

        if (
            size_mode
            and request.user
            and hasattr(request.user, 'chest')
            and request.user.chest
        ):
            user_chest = request.user.chest
            recommendations = get_size_recommendations(user_chest, product)

        category_button_class = CATEGORY_BUTTON_CLASSES.get(
            product.category.name.lower(), 'btn-outline-dark'
        )

        context = {
            'product': product,
            'measurement_form': form,
            'recommendations': recommendations,
            'category_button_class': category_button_class,
            'size_mode': size_mode,
            'show_size_mode_toggle': True,
            'reopen_measurement_modal': True,  # used to trigger modal on error
        }
        return render(request, 'products/product_detail.html', context)
