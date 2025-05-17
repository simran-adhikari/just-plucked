from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product
from master.models import Category


from django.shortcuts import get_object_or_404, render

def product_detail(request, slug):
    # Fetch the product by slug
    product = get_object_or_404(Product, slug=slug)
    search_query = request.GET.get('search', '')

    # Build base context
    context = {
        'product': product,
        'search_query': search_query,
    }

    # Only calculate/send discount percent if there's a discounted_price
    if product.discounted_price and product.discounted_price < product.regular_price:
        discount_percent = ((product.regular_price - product.discounted_price)
                            / product.regular_price) * 100
        # round off to 2 decimal places, if you like
        context['discount_percent'] = round(discount_percent, 2)

    return render(request,
                  'website/product/product_detail.html',
                  context)


def product_list(request):
    # grab both GET-params
    category_id = request.GET.get('category')
    search_term = request.GET.get('search', '').strip()

    # start with everything…
    products = Product.objects.all()

    # …narrow by category if provided
    if category_id:
        products = products.filter(category_id=category_id)

    # …and then by your search term
    if search_term:
        products = products.filter(
            Q(name__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(tags__name__icontains=search_term)
        ).distinct()

    return render(request, 'website/product/product_list.html', {
        'categories':       Category.objects.all(),
        'products':         products,
        'selected_category': category_id or '',
        'search_term':      search_term,
    })

def category_detail(request, slug):
    # Fetch the category by slug
    category = get_object_or_404(Category, slug=slug)

    # Get search query and other filters from request
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')  # Default sort by product name
    filter_price_min = request.GET.get('price_min', None)
    filter_price_max = request.GET.get('price_max', None)

    # Start with products in the selected category
    products = category.products.all()

    # Apply search filter if there is a search query
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()

     
    if filter_price_min:
        products = products.filter(regular_price__gte=filter_price_min)
    if filter_price_max:
        products = products.filter(regular_price__lte=filter_price_max)

     
    if sort_by == 'price_asc':
        products = products.order_by('regular_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-regular_price')
    elif sort_by == 'name':
        products = products.order_by('name')
    elif sort_by == 'created':
        products = products.order_by('created')

    return render(request, 'website/product/category_detail.html', {
        'category': category,
        'products': products,
        'search_query': search_query,
        'sort_by': sort_by,
        'filter_price_min': filter_price_min,
        'filter_price_max': filter_price_max,
    })
