# orders/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Count

from .models import Order, OrderItem
from website.models import HomepageData
from products.models import Product


def _rebuild_homepage_data():
    # we assume you have exactly one HomepageData row (e.g. pk=1)
    homepage, _ = HomepageData.objects.get_or_create(pk=1)

    # 1) Popular = top 5 products by all-time order count
    popular_qs = (
        Product.objects
               .annotate(total_orders=Count('orderitem'))
               .order_by('-total_orders')[:5]
    )
    homepage.popular.set(popular_qs)

    # 2) Trending = top 5 products by orders in the last 7 days
    week_ago = timezone.now() - timezone.timedelta(days=7)
    trending_qs = (
        Product.objects
               .filter(orderitem__order__created_at__gte=week_ago)
               .annotate(recent_orders=Count('orderitem'))
               .order_by('-recent_orders')[:5]
    )
    homepage.trending.set(trending_qs)

    homepage.save()


@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def refresh_homepage_on_order_change(sender, **kwargs):
    """
    Whenever an Order or OrderItem is created/updated/deleted,
    recalculate homepage.trending and homepage.popular.
    """
    _rebuild_homepage_data()
