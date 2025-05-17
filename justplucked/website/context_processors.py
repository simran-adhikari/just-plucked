from master.models import Category
from order.models import Cart, CartItem, Wishlist, WishlistItem

def example_context(request):
    user = request.user
    categories = Category.objects.all()

    cart_items = []
    wishlist_items = []

    if user.is_authenticated:
        # get the active cart (the one not yet checked out)
        try:
            cart = Cart.objects.get(user=user, checked_out=False)
            # fetch all items in that cart
            cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        except Cart.DoesNotExist:
            cart_items = []

        # get (or create) the user’s wishlist
        try:
            wishlist = Wishlist.objects.get(user=user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist).select_related('product')
        except Wishlist.DoesNotExist:
            wishlist_items = []

    return {
        'categories':       categories,
        'cart_items':       cart_items,
        'wishlist_items':   wishlist_items,
        # if you still want simple counts:
        'cart_count':       len(cart_items),
        'wishlist_count':   len(wishlist_items),
    }
