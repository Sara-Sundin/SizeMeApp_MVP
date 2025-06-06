from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm

from sizemeapp.utils.recommendations import get_size_recommendations
from accounts.forms import MeasurementUpdateForm


# Mapping category names to CSS classes for button styling
CATEGORY_BUTTON_CLASSES = {
    'tshirts': 'cta-btn--primary',
    'shirts': 'cta-btn--tertiary',
    'sweatshirts': 'cta-btn--black',
}


def all_products(request):
    """
    Display all products with optional sorting, filtering by category,
    and search by name or description.
    """
    products = Product.objects.all()
    query = request.GET.get('q')
    category_names = request.GET.get('category')
    sort_param = request.GET.get('sort', 'None_None')

    selected_category = None
    category_button_class = None
    current_categories = None

    # Mapping from sort dropdown values to ORM sort expressions
    sort_map = {
        'name_asc': 'lower_name',
        'name_desc': '-lower_name',
        'price_asc': 'price',
        'price_desc': '-price',
        'category_asc': 'category__name',
        'category_desc': '-category__name',
    }

    # Apply sorting logic
    if sort_param in sort_map:
        sort_key = sort_map[sort_param]
        if 'lower_name' in sort_key:
            products = products.annotate(lower_name=Lower('name'))
        products = products.order_by(sort_key)
    else:
        sort_param = 'None_None'

    # Filter by category if provided
    if category_names:
        category_list = category_names.split(',')
        products = products.filter(category__name__in=category_list)
        current_categories = Category.objects.filter(name__in=category_list)

        if current_categories.exists():
            selected_category = current_categories.first().friendly_name
            category_button_class = CATEGORY_BUTTON_CLASSES.get(
                current_categories.first().name.lower(), 'btn-outline-dark'
            )

    # Filter by search query
    if query:
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))

    context = {
        'products': products,
        'search_term': query,
        'current_categories': current_categories,
        'current_sorting': sort_param,
        'selected_category': selected_category,
        'category_button_class': category_button_class,
        'category_button_classes': CATEGORY_BUTTON_CLASSES,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    Display a single product detail page.
    Includes size recommendations if size mode is active.
    """
    product = get_object_or_404(Product, pk=product_id)
    recommendations = []

    size_mode = request.session.get('size_mode', False)

    if (
        size_mode and request.user.is_authenticated and
        hasattr(request.user, 'chest') and request.user.chest
    ):
        recommendations = get_size_recommendations(
            request.user.chest, product
        )

    category_button_class = CATEGORY_BUTTON_CLASSES.get(
        product.category.name.lower(), 'btn-outline-dark'
    )

    show_webshop_measurements_success = request.session.pop(
        'show_webshop_measurements_success', False
    )
    show_size_mode_entered_modal = request.session.pop(
        'size_mode_entered', False
    )
    show_size_mode_exited_modal = request.session.pop(
        'size_mode_exited', False
    )

    measurement_form = (
        MeasurementUpdateForm(instance=request.user)
        if request.user.is_authenticated else None
    )

    context = {
        'product': product,
        'recommendations': recommendations,
        'category_button_class': category_button_class,
        'size_mode': size_mode,
        'show_webshop_measurements_success': show_webshop_measurements_success,
        'show_size_mode_entered_modal': show_size_mode_entered_modal,
        'show_size_mode_exited_modal': show_size_mode_exited_modal,
        'show_size_mode_toggle': True,
        'measurement_form': measurement_form,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """
    View for superusers to add a new product.
    Handles both displaying the form and processing the POST request.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('webshop'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error
        (request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """
    View for superusers to edit an existing product.
    Prefills the form with the current product data.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('webshop'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error
        (request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product
    })


@login_required
def delete_product(request, product_id):
    """
    View for superusers to delete an existing product.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('webshop'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
