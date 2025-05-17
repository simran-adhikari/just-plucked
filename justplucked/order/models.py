from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import uuid
from django.utils import timezone

User = get_user_model()

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Coupon Code"))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount (%)"))
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    valid_from = models.DateTimeField(verbose_name=_("Valid From"))
    valid_to = models.DateTimeField(verbose_name=_("Valid To"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and (self.valid_from <= now <= self.valid_to)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts", verbose_name=_("User"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    checked_out = models.BooleanField(default=False, verbose_name=_("Checked Out"))
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Coupon"))

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ['-created']

    def __str__(self):
        return f"Cart #{self.id} - {self.user}"

    @property
    def total(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("Cart"))
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantity"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    @property
    def total_price(self):
        return self.product.discounted_price or self.product.regular_price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        CONFIRMED = 'confirmed', _('Confirmed')
        PROCESSING = 'processing', _('Processing')
        SHIPPED = 'shipped', _('Shipped')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')
        RETURNED = 'returned', _('Returned')

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("UUID"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", verbose_name=_("User"))
    invoice_id = models.CharField(max_length=50, unique=True, verbose_name=_("Invoice ID"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Order Status"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Subtotal"))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Tax"))
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Shipping Charge"))
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"))
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Applied Coupon"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-created']

    def __str__(self):
        return f"Order #{self.invoice_id}"

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = self.generate_invoice_id()
        super().save(*args, **kwargs)

    def generate_invoice_id(self):
        return f"INV-{self.created.strftime('%Y%m%d')}-{self.id:06d}"


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name=_("Order"))
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, verbose_name=_("Product"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    farmer = models.ForeignKey("farmer.Farmer", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Farmer"))
     

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    @property
    def total_price(self):
        return self.price * self.quantity


class Delivery(models.Model):
    class Method(models.TextChoices):
        PICKUP = 'pickup', _('Pickup')
        HOME = 'home', _('Home Delivery')
        COURIER = 'courier', _('Courier')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        OUT_FOR_DELIVERY = 'out_for_delivery', _('Out for Delivery')
        DELIVERED = 'delivered', _('Delivered')
        FAILED = 'failed', _('Failed')

    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery", verbose_name=_("Order"))
    address = models.TextField(verbose_name=_("Delivery Address"))
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.HOME, verbose_name=_("Delivery Method"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Delivery Status"))
    estimated_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Estimated Delivery"))
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Delivered At"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")

    def __str__(self):
        return f"Delivery for {self.order}"


class Payment(models.Model):
    class Method(models.TextChoices):
        COD = 'cod', _('Cash on Delivery')
        ESEWA = 'esewa', _('eSewa')
        STRIPE = 'stripe', _('Stripe')
        BANK = 'bank', _('Bank Transfer')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')

    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", verbose_name=_("Order"))
    method = models.CharField(max_length=20, choices=Method.choices, verbose_name=_("Payment Method"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name=_("Payment Status"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount Paid"))
    transaction_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Transaction ID"))
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Paid At"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"Payment for {self.order.invoice_id}"


class Refund(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="refunds", verbose_name=_("Order"))
    reason = models.TextField(verbose_name=_("Refund Reason"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Refund Amount"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Refund Date"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))

    class Meta:
        verbose_name = _("Refund")
        verbose_name_plural = _("Refunds")

    def __str__(self):
        return f"Refund for {self.order}"


class OrderStatusHistory(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history", verbose_name=_("Order"))
    previous_status = models.CharField(max_length=20, verbose_name=_("Previous Status"))
    new_status = models.CharField(max_length=20, verbose_name=_("New Status"))
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Changed At"))

    class Meta:
        verbose_name = _("Order Status History")
        verbose_name_plural = _("Order Status Histories")
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.order.invoice_id}: {self.previous_status} → {self.new_status}"


class Shipment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SHIPPED = 'shipped', _('Shipped')
        IN_TRANSIT = 'in_transit', _('In Transit')
        DELIVERED = 'delivered', _('Delivered')
        LOST = 'lost', _('Lost')

    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="shipment", verbose_name=_("Order"))
    tracking_number = models.CharField(max_length=255, unique=True, verbose_name=_("Tracking Number"))
    carrier = models.CharField(max_length=100, verbose_name=_("Carrier"))
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING, verbose_name=_("Shipment Status"))
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Shipped At"))
    estimated_arrival = models.DateTimeField(null=True, blank=True, verbose_name=_("Estimated Arrival"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Shipment")
        verbose_name_plural = _("Shipments")

    def __str__(self):
        return f"Shipment #{self.tracking_number}"


class TrackingUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="updates", verbose_name=_("Shipment"))
    status = models.CharField(max_length=50, choices=Shipment.Status.choices, default=Shipment.Status.PENDING, verbose_name=_("Update Status"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    update_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Update Time"))
    note = models.TextField(blank=True, null=True, verbose_name=_("Note"))

    class Meta:
        verbose_name = _("Tracking Update")
        verbose_name_plural = _("Tracking Updates")
        ordering = ['-update_time']

    def __str__(self):
        return f"Update for {self.shipment.tracking_number} - {self.status}"


class Wishlist(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='wishlist',
        verbose_name=_("User")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return f"Wishlist of {self.user.email}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")
        unique_together = ('wishlist', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user}'s wishlist"