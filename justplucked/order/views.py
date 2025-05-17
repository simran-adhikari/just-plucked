from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Cart, CartItem, Order, Coupon, Delivery, Payment, Refund, OrderStatusHistory, Shipment,OrderItem,Wishlist,WishlistItem
from products.models import Product
import stripe
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
    cart_items = cart.items.all()
    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            cart.coupon = coupon
            cart.save()
            messages.success(request, "Coupon applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code")
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'website/order/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, checked_out=False)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, "Product added to cart!")
    return redirect('cart_view')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart_view')

@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    
    return redirect('cart_view')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, checked_out=False)
    
    if request.method == 'POST':
        try:
            
            intent = stripe.PaymentIntent.create(
                amount=int(cart.total * 100),  
                currency='usd',
                metadata={'user_id': request.user.id}
            )
            
            
            order = Order.objects.create(
                user=request.user,
                subtotal=cart.total,
                total=cart.total,
                coupon=cart.coupon
            )
            
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discounted_price or item.product.regular_price,
                    farmer=item.product.farmer
                )
            
            
            cart.checked_out = True
            cart.save()
             
            
            
            
            Payment.objects.create(
                order=order,
                method='stripe',
                amount=cart.total,
                status='pending'
            )
            
            
            Delivery.objects.create(
                order=order,
                address=request.user.profile.shipping_address,
                status='pending'
            )
            
            
            context = {
                'client_secret': intent.client_secret,
                'order': order,  
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
            }
            return render(request, 'website/order/payment.html', context)
        
        except Exception as e:
            messages.error(request, f"Error processing payment: {str(e)}")
            return redirect('checkout')
    
    context = {
        'cart': cart,
    }
    return render(request, 'website/order/checkout.html', context)

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment = order.payment
    payment.status = 'paid'
    payment.paid_at = timezone.now()
    payment.save()

    order.status = 'confirmed'
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        previous_status='pending',
        new_status='confirmed'
    )

    messages.success(request, "Payment successful! Your order is being processed.")

    # —— NEW: delete the old cart ——
    Cart.objects.filter(user=request.user, checked_out=False).delete()

    return redirect('order_detail', order_id=order.id)
@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    payment = order.payment
    payment.status = 'failed'
    payment.save()
    
    messages.error(request, "Payment failed. Please try again.")
    return redirect('checkout')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'website/order/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'website/order/order_history.html', {'orders': orders})

@login_required
def track_shipment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    shipment = getattr(order, 'shipment', None)
    return render(request, 'website/order/track_shipment.html', {'order': order, 'shipment': shipment})

@login_required
def initiate_refund(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        Refund.objects.create(
            order=order,
            reason=reason,
            amount=order.total,
        )
        messages.success(request, "Refund request submitted successfully!")
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'website/order/initiate_refund.html', {'order': order})

@login_required
def order_status_history(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    history = order.status_history.all().order_by('-changed_at')
    return render(request, 'website/order/order_status_history.html', {'order': order, 'history': history})


stripe.api_key = 'sk_test_51RI4mmIHchYkQBZznvLcrykRmttOGnA1ZRX2bhfuTLl4HuqCSawsQxK6pXTtrFrN1dXDkW5eyn13AAFXUnDpiGVa00dxP2bHml'  

@csrf_exempt  
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            
            intent = stripe.PaymentIntent.create(
                amount=1000,  
                currency='usd',
            )
            return JsonResponse({'clientSecret': intent.client_secret,"status":"success"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


 
@csrf_exempt  
def create_order(request, cart_id):
    try:       
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        cart = Cart.objects.get(id=cart_id, user=request.user)   
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            invoice_id=f"INV {cart_id}",
            status=Order.Status.PENDING,
            subtotal=cart.total,
            total=cart.total,  
            coupon=cart.coupon,
        )       
        
        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price or item.product.regular_price,
                farmer=item.product.farmer  
            )
        
        # Mark cart as checked out
        cart.checked_out = True
        cart.save()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect_url': reverse('order_detail', args=[order.id])
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product')
    return render(request, 'website/order/wishlist.html', {'wishlist': wishlist, 'items': items})

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if not WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
            WishlistItem.objects.create(wishlist=wishlist, product=product)
            message = "Product added to wishlist"
            success = True
        else:
            message = "Product already in wishlist"
            success = False

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': success, 'message': message, 'redirect_url': '/wishlist'})

        return redirect('/wishlist')
    
    return redirect('product_detail', pk=product_id)

@login_required
def remove_from_wishlist(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
        item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Product removed from wishlist'})
        
        return redirect('wishlist')
    return redirect('wishlist')