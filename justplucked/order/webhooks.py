from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
import json
from .models import *
from django.conf import settings
from django.utils import timezone
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle payment intent events
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_succeeded(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_failed(payment_intent)

    return HttpResponse(status=200)

def handle_payment_succeeded(payment_intent):
    order_id = payment_intent['metadata'].get('order_id')
    try:
        order = Order.objects.get(invoice_id=order_id)
        order.payment.status = 'paid'
        order.payment.paid_at = timezone.now()
        order.payment.save()
        
        order.status = 'confirmed'
        order.save()
        OrderStatusHistory.objects.create(
            order=order,
            previous_status='pending',
            new_status='confirmed'
        )
    except Order.DoesNotExist:
        pass

def handle_payment_failed(payment_intent):
    order_id = payment_intent['metadata'].get('order_id')
    try:
        order = Order.objects.get(invoice_id=order_id)
        order.payment.status = 'failed'
        order.payment.save()
        
        order.status = 'cancelled'
        order.save()
        OrderStatusHistory.objects.create(
            order=order,
            previous_status='pending',
            new_status='cancelled'
        )
    except Order.DoesNotExist:
        pass