from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Cart URLs
    path('cart/', login_required(views.cart_view), name='cart_view'),
    path('cart/add/<int:product_id>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('cart/remove/<int:item_id>/', login_required(views.remove_from_cart), name='remove_from_cart'),
    path('cart/update/<int:item_id>/', login_required(views.update_cart_item), name='update_cart_item'),
    
    # Checkout and Payment URLs
    path('checkout/', login_required(views.checkout), name='checkout'),
    path('payment/success/<int:order_id>/', login_required(views.payment_success), name='payment_success'),
    path('payment/failed/<int:order_id>/', login_required(views.payment_failed), name='payment_failed'),
    
    # Order Management URLs
    path('orders/', login_required(views.order_history), name='order_history'),
    path('orders/<int:order_id>/', login_required(views.order_detail), name='order_detail'),
    path('orders/<int:order_id>/track/', login_required(views.track_shipment), name='track_shipment'),
    path('orders/<int:order_id>/refund/', login_required(views.initiate_refund), name='initiate_refund'),
    path('orders/<int:order_id>/history/', login_required(views.order_status_history), name='order_status_history'),

    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('create-order/<int:cart_id>', views.create_order, name='create_order'),
    path('wishlist', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


]