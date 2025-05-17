from django.db import models
from django.utils.text import slugify
from django.db.models import Avg
from farmer.models import Farmer
from master.models import Category, Tag, UnitOfMeasure


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Product Name")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Product Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='products/', verbose_name="Product Image")
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT, blank=True, null=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Regular Price", default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Discounted Price", null=True, blank=True)
    product_average_rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        verbose_name="Average Rating"
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    shelf_life_remaining = models.PositiveIntegerField(
        help_text="Remaining shelf life in days",
        verbose_name="Remaining Shelf Life (in days)"
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def reduce_stock_due_to_expiry(self):
        if self.shelf_life_remaining <= 0:
            self.stock_quantity = 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.reduce_stock_due_to_expiry()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Product"
    )
    image = models.ImageField(upload_to='product_images/', verbose_name="Product Image")
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Alt Text")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Product"
    )
    user = models.CharField(max_length=255, verbose_name="User")
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Rating"
    )
    review = models.TextField(blank=True, null=True, verbose_name="Review")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Review for {self.product.name} by {self.user}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        avg = self.product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        self.product.product_average_rating = round(avg, 2)
        self.product.save(update_fields=['product_average_rating'])

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        avg = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        product.product_average_rating = round(avg, 2)
        product.save(update_fields=['product_average_rating'])

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"


class ProductPricingHistory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="pricing_history",
        verbose_name="Product"
    )
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Old Price")
    new_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="New Price")
    change_date = models.DateTimeField(auto_now_add=True, verbose_name="Change Date")

    def __str__(self):
        return f"Price change for {self.product.name} on {self.change_date}"

    class Meta:
        verbose_name = "Product Pricing History"
        verbose_name_plural = "Product Pricing History"


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="Product"
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    shelf_life_remaining = models.PositiveIntegerField(
        help_text="Remaining shelf life in days",
        verbose_name="Remaining Shelf Life (in days)"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Inventory for {self.product.name}"

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
