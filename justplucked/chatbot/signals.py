from django.apps import AppConfig
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings

class ChatbotConfig(AppConfig):
    name = 'chatbot'

    def ready(self):
        chatbot = ChatBot(**settings.CHATTERBOT)
        
        # Your training data
        from chatterbot.trainers import ListTrainer
        trainer = ListTrainer(chatbot)
        
        custom_data = [
    # Product inquiries
    "What products do you sell?",
    "We sell fresh vegetables, fruits, grains, and dairy products directly from farmers.",
    "What kind of items do you offer?",
    "Our marketplace offers farm-fresh produce including seasonal vegetables, organic fruits, whole grains, and artisanal dairy products.",
    "Do you have organic products?",
    "Yes, many of our farmers provide organic produce. Look for the 'Organic' label on product pages.",
    "Where do your products come from?",
    "All our products come directly from local farmers and partner farms to ensure freshness and quality.",
    
    # Ordering process
    "How do I place an order?",
    "You can place an order by browsing our product catalog and adding items to your cart. Once you're ready, proceed to checkout.",
    "What's the ordering process?",
    "Simply browse our products, add items to your cart, and complete checkout with your delivery and payment details.",
    "Can I order by phone?",
    "Currently we only accept online orders through our website or mobile app for better order tracking.",
    
    # Delivery information
    "What is the delivery time?",
    "Delivery times vary depending on your location. Typically, deliveries take 2-3 days.",
    "How long does shipping take?",
    "Most orders arrive within 2-3 business days. You'll receive tracking information once your order ships.",
    "Do you offer same-day delivery?",
    "Same-day delivery is available in some areas. Please check the delivery options at checkout.",
    "What are your delivery hours?",
    "Deliveries typically occur between 8 AM and 8 PM, Monday through Saturday.",
    "Can I specify a delivery time?",
    "Yes, during checkout you can select preferred delivery time windows where available.",
    
    # Order modifications
    "Can I cancel my order?",
    "You can cancel your order within 24 hours of placing it. After that, cancellation is not possible.",
    "How do I change my order?",
    "You can modify your order within 1 hour of placing it by contacting customer support.",
    "What if I want to add items to my order?",
    "For order additions, please place a new order. We cannot modify existing orders after 1 hour.",
    
    # Payment options
    "How do I pay for my order?",
    "We accept payments via credit card, debit card, and online banking. You can select your preferred method at checkout.",
    "What payment methods do you accept?",
    "We accept Visa, Mastercard, American Express, PayPal, and direct bank transfers.",
    "Do you accept cash on delivery?",
    "Currently we only accept digital payments for all orders.",
    "Is my payment information secure?",
    "Yes, we use industry-standard encryption to protect all payment transactions.",
    
    # Pricing and discounts
    "Do you offer discounts on bulk orders?",
    "Yes, we offer discounts on bulk orders. Please contact our support team for more details.",
    "Are there any promo codes available?",
    "We occasionally run promotions. Check our website banner or subscribe to our newsletter for current offers.",
    "Do you have a loyalty program?",
    "Yes! Our FarmFresh Rewards program gives you points for every purchase that can be redeemed for discounts.",
    
    # Customer support
    "How can I contact customer support?",
    "You can contact customer support by emailing support@farmersmarket.com or calling 1-800-123-4567.",
    "What are your support hours?",
    "Our customer support team is available 7 AM to 10 PM daily, including weekends.",
    "Do you have live chat support?",
    "Yes, live chat is available on our website during business hours (7 AM to 10 PM).",
    
    # Delivery locations
    "Do you deliver internationally?",
    "Currently, we only deliver within the country. We plan to expand internationally soon!",
    "What areas do you serve?",
    "We deliver to all major cities and surrounding areas. Enter your zip code during checkout to confirm availability.",
    "Do you deliver to rural areas?",
    "We deliver to most rural areas, though delivery times may be longer. Check your address during checkout.",
    
    # Issues and returns
    "What should I do if my order is damaged?",
    "If your order is damaged, please contact customer support immediately, and we will issue a refund or replacement based on your preference.",
    "My order is missing items, what do I do?",
    "Please contact customer support with your order number and details of missing items for immediate assistance.",
    "What's your return policy?",
    "We accept returns of damaged or incorrect items within 7 days of delivery. Contact support to initiate a return.",
    "The produce I received isn't fresh",
    "We guarantee fresh products. If you're unsatisfied, please contact us for a refund or replacement.",
    
    # Account management
    "How do I create an account?",
    "You can create an account during checkout or by visiting the 'Sign Up' page on our website.",
    "I forgot my password",
    "Click 'Forgot Password' on the login page to reset your password via email.",
    "Can I save my payment information?",
    "Yes, you can securely save payment methods in your account for faster checkout.",
    
    # Miscellaneous
    "Do you offer gift cards?",
    "Yes! Digital gift cards are available in any amount on our website's Gift Cards page.",
    "Can I schedule recurring orders?",
    "We offer subscription options for many products. Look for the 'Subscribe' button on product pages.",
    "How do I provide feedback?",
    "We welcome feedback! You can rate products after purchase or email feedback@farmersmarket.com.",
    "Are your products sustainably sourced?",
    "We prioritize sustainable farming practices and work with farmers who share our environmental values."
]
        
        print("Training chatbot...")
        trainer.train(custom_data)
        print("Chatbot training completed!")