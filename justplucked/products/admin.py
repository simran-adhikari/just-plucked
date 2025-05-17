from django.contrib import admin
from .models import Product, ProductImage, ProductReview, ProductPricingHistory, Inventory

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to show
    verbose_name = "Product Image"
    verbose_name_plural = "Product Images"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show product images related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset


# Inline for Product Reviews
class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 1
    verbose_name = "Product Review"
    verbose_name_plural = "Product Reviews"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show reviews related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset


# Inline for Product Pricing History
class ProductPricingHistoryInline(admin.TabularInline):
    model = ProductPricingHistory
    extra = 1
    verbose_name = "Product Pricing History"
    verbose_name_plural = "Product Pricing History"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show pricing history related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset


# Inline for Inventory
class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1
    verbose_name = "Inventory"
    verbose_name_plural = "Inventories"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show inventory related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset


# Admin for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'regular_price', 'discounted_price', 'stock_quantity', 'shelf_life_remaining', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('name',)
    
    exclude=("created","updated")
    inlines = [ProductImageInline, ProductReviewInline, ProductPricingHistoryInline, InventoryInline]
 

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show products related to the logged-in farmer
            return queryset.filter(farmer__user=request.user)
        return queryset


# Register Product model with the custom admin
admin.site.register(Product, ProductAdmin)


# Admin for ProductImage
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text', 'created')
    search_fields = ('product__name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show images related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset

admin.site.register(ProductImage, ProductImageAdmin)


# Admin for ProductReview
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('rating', 'created')
    search_fields = ('user', 'product__name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show reviews related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset

admin.site.register(ProductReview, ProductReviewAdmin)


# Admin for ProductPricingHistory
class ProductPricingHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'old_price', 'new_price', 'change_date')
    search_fields = ('product__name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show pricing history related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset

admin.site.register(ProductPricingHistory, ProductPricingHistoryAdmin)


# Admin for Inventory
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock_quantity', 'shelf_life_remaining', 'created', 'updated')
    search_fields = ('product__name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.groups.filter(name='farmer').exists():
            # Only show inventory related to the logged-in farmer's products
            return queryset.filter(product__farmer__user=request.user)
        return queryset

admin.site.register(Inventory, InventoryAdmin)
