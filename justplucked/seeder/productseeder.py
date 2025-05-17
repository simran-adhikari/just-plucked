import random
from django.utils import timezone
from django.utils.text import slugify
from products.models import Product, ProductImage, ProductReview, ProductPricingHistory, Inventory
from master.models import Category, UnitOfMeasure, Tag
from farmer.models import Farmer

def create_product_dummy_data():
    # Get existing data needed for relationships
    categories = Category.objects.all()
    units = UnitOfMeasure.objects.all()
    tags = Tag.objects.all()
    farmers = Farmer.objects.all()
    
    if not categories or not units or not tags or not farmers:
        print("Please make sure you have created master data and farmers first")
        return

    # List of realistic product names for different categories
    product_names = [
        "Organic Apples", "Bananas", "Strawberries", "Mangoes", "Pineapples",
        "Organic Carrots", "Broccoli", "Spinach", "Tomatoes", "Bell Peppers",
        "Fresh Milk", "Cheddar Cheese", "Greek Yogurt", "Butter", "Cottage Cheese",
        "Whole Wheat Bread", "Brown Rice", "Quinoa", "Oats", "Whole Grain Pasta",
        "Chicken Breast", "Grass-fed Beef", "Pork Chops", "Turkey", "Lamb"
    ]

    products = []
    for i in range(20):
        # Basic product info
        name = product_names[i]
        farmer = random.choice(farmers)
        regular_price = round(random.uniform(1.99, 19.99), 2)
        discounted_price = round(regular_price * random.uniform(0.7, 0.95), 2) if random.choice([True, False]) else None
        stock = random.randint(0, 100)
        shelf_life = random.randint(1, 365)
        
        # Generate slug and ensure uniqueness
        slug = slugify(name)
        if Product.objects.filter(slug=slug).exists():
            slug = f"{slug}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create product
        product = Product.objects.create(
            name=name,
            slug=slug,
            farmer=farmer,
            description=f"High quality {name.lower()} from {farmer.full_name}. Product description details here.",
            regular_price=regular_price,
            discounted_price=discounted_price,
            stock_quantity=stock,
            shelf_life_remaining=shelf_life
        )

        # Set fields for ForeignKeys (category, unit_of_measure)
        product.category = random.choice(categories)
        product.unit_of_measure = random.choice(units)
        product.tags.set(random.sample(list(tags), random.randint(1, 3)))
        product.save()

        products.append(product)
        print(f"Created Product: {product} (Farmer: {farmer.full_name})")

        # Create 1-3 product images
        for img_num in range(1, random.randint(2, 4)):
            ProductImage.objects.create(
                product=product,
                alt_text=f"{name} image {img_num}"
            )
            print(f"  Created ProductImage for {product}")

        # Create 0-5 reviews per product
        for review_num in range(random.randint(0, 5)):
            ProductReview.objects.create(
                product=product,
                user=f"User{review_num}",
                rating=random.randint(1, 5),
                review=f"This is a sample review for {name}. It's {'great' if random.choice([True, False]) else 'average'}."
            )
            print(f"  Created ProductReview for {product}")

        # Create pricing history (1-3 entries per product)
        price_changes = [regular_price]
        if discounted_price:
            price_changes.append(discounted_price)
        
        for j in range(1, random.randint(2, 4)):
            old_price = price_changes[-1]
            new_price = round(old_price * random.uniform(0.9, 1.2), 2)
            price_changes.append(new_price)
            
            ProductPricingHistory.objects.create(
                product=product,
                old_price=old_price,
                new_price=new_price,
                change_date=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
            )
            print(f"  Created ProductPricingHistory for {product}")

        # Create inventory record
        Inventory.objects.create(
            product=product,
            stock_quantity=stock,
            shelf_life_remaining=shelf_life
        )
        print(f"  Created Inventory record for {product}")

    print(f"\nSuccessfully created {len(products)} products with related data!")

if __name__ == "__main__":
    create_product_dummy_data()
