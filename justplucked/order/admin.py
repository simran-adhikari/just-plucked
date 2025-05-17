from django.contrib import admin
from .models import Coupon, Cart, CartItem, Order, OrderItem, Payment, Refund, Delivery, Shipment, TrackingUpdate, Wishlist, WishlistItem

# Admin for Coupon
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'valid_from', 'valid_to', 'created', 'updated')
    search_fields = ('code',)
    list_filter = ('active', 'valid_from', 'valid_to')

admin.site.register(Coupon, CouponAdmin)


# Admin for Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'checked_out', 'created', 'updated', 'total')
    search_fields = ('user__email',)
    list_filter = ('checked_out',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show carts related to the logged-in farmer's products
            return queryset.filter(user=request.user)
        return queryset

admin.site.register(Cart, CartAdmin)


# Admin for CartItem
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'updated')
    search_fields = ('cart__id', 'product__name')
    list_filter = ('cart__checked_out',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show cart items related to the logged-in farmer's products
            return queryset.filter(cart__user=request.user)
        return queryset

    def total_price(self, obj):
        return obj.product.discounted_price or obj.product.regular_price * obj.quantity
    total_price.admin_order_field = 'total_price'

admin.site.register(CartItem, CartItemAdmin)


# Admin for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'user', 'status', 'total', 'created', 'updated')
    search_fields = ('invoice_id', 'user__email')
    list_filter = ('status', 'created')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show orders related to the logged-in farmer's order items
            return queryset.filter(items__farmer__user=request.user)
        return queryset

admin.site.register(Order, OrderAdmin)


# Admin for OrderItem (Farmer-specific details)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'farmer', 'total_price')
    search_fields = ('order__invoice_id', 'product__name')
    list_filter = ('order__status',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show OrderItems where the farmer is related to the product in the OrderItem
            return queryset.filter(farmer__user=request.user)
        return queryset

    def total_price(self, obj):
        return obj.price * obj.quantity
    total_price.admin_order_field = 'price'

admin.site.register(OrderItem, OrderItemAdmin)


# Admin for Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'method', 'status', 'amount', 'created', 'updated')
    search_fields = ('order__invoice_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show payments for orders related to the logged-in farmer
            return queryset.filter(order__items__farmer__user=request.user)
        return queryset

admin.site.register(Payment, PaymentAdmin)


# Admin for Refund
class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason', 'amount', 'approved', 'created', 'updated')
    search_fields = ('order__invoice_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show refunds for orders related to the logged-in farmer
            return queryset.filter(order__items__farmer__user=request.user)
        return queryset

admin.site.register(Refund, RefundAdmin)


# Admin for Delivery
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'address', 'method', 'status', 'created', 'updated')
    search_fields = ('order__invoice_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show deliveries related to orders placed by the logged-in farmer
            return queryset.filter(order__items__farmer__user=request.user)
        return queryset

admin.site.register(Delivery, DeliveryAdmin)


# Admin for Shipment
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'tracking_number', 'carrier', 'status', 'shipped_at', 'estimated_arrival', 'created', 'updated')
    search_fields = ('order__invoice_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show shipments related to orders placed by the logged-in farmer
            return queryset.filter(order__items__farmer__user=request.user)
        return queryset

admin.site.register(Shipment, ShipmentAdmin)


# Admin for TrackingUpdate
class TrackingUpdateAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'status', 'location', 'update_time', 'note')
    search_fields = ('shipment__tracking_number',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show tracking updates related to shipments for the logged-in farmer's orders
            return queryset.filter(shipment__order__items__farmer__user=request.user)
        return queryset

admin.site.register(TrackingUpdate, TrackingUpdateAdmin)


# Admin for Wishlist
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show wishlists belonging to the logged-in farmer
            return queryset.filter(user=request.user)
        return queryset

admin.site.register(Wishlist, WishlistAdmin)


# Admin for WishlistItem
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'added_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show wishlist items for the logged-in farmer's products
            return queryset.filter(wishlist__user=request.user)
        return queryset

admin.site.register(WishlistItem, WishlistItemAdmin)
