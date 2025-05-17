from django.shortcuts import render
from django.db.models import Sum, F
from products.models import Product
from order.models import Order, OrderItem
from farmer.models import Farmer

def farmer_dashboard_data(request):
    """
    Context processor that provides dashboard data based on user type.
    Returns total number of products, orders, and revenue.
    For superusers: total for all farmers.
    For farmers: total specific to the logged-in farmer.
    """
    data = {}

    if not request.user.is_authenticated:
        return data

    if request.user.is_superuser:
        # Superuser: total products, orders, and revenue for all farmers
        data['farmer'] = Farmer.objects.count()
        data['total_products'] = Product.objects.count()
        data['total_orders'] = Order.objects.count()
        data['total_revenue'] = (
            OrderItem.objects.annotate(
                item_total=F('price') * F('quantity')
            ).aggregate(total_revenue=Sum('item_total'))['total_revenue'] or 0
        )
    elif hasattr(request.user, 'farmer'):
        farmer = request.user.farmer
        data['total_products'] = Product.objects.filter(farmer=farmer).count()
        data['total_orders'] = Order.objects.filter(items__farmer=farmer).distinct().count()
        data['total_revenue'] = (
            OrderItem.objects.filter(farmer=farmer)
            .annotate(item_total=F('price') * F('quantity'))
            .aggregate(total_revenue=Sum('item_total'))['total_revenue'] or 0
        )

    return data
