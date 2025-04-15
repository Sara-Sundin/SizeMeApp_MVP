from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


CATEGORY_BUTTON_CLASSES = {
    'tshirts': 'cta-btn--primary',
    'shirts': 'cta-btn--tertiary',
    'hats': 'cta-btn--black',
}

def all_products(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    category_names = request.GET.get('category')
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')

    selected_category = None
    category_button_class = None

    if sort:
        sortkey = sort
        if sortkey == 'name':
            products = products.annotate(lower_name=Lower('name'))
            sortkey = 'lower_name'
        elif sortkey == 'category':
            sortkey = 'category__name'
        if direction == 'desc':
            sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)

    if category_names:
        category_list = category_names.split(',')
        products = products.filter(category__name__in=category_list)
        current_categories = Category.objects.filter(name__in=category_list)

        # Use first category for active display
        if current_categories:
            selected_category = current_categories[0].friendly_name
            category_key = current_categories[0].name  # match lowercase slug name
            category_button_class = CATEGORY_BUTTON_CLASSES.get(category_key, 'btn-outline-dark')
    else:
        current_categories = None

    if query:
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': current_categories,
        'current_sorting': current_sorting,
        'selected_category': selected_category,
        'category_button_class': category_button_class,
        'category_button_classes': CATEGORY_BUTTON_CLASSES,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ Show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))