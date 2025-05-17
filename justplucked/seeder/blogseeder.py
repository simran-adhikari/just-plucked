import random
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Category, Tag, Blog

def create_blog_dummy_data():
    # Create 7 Categories
    categories = []
    category_names = [
        "Agriculture", "Technology", "Farming Techniques", 
        "Organic Farming", "Livestock", "Crop Rotation", 
        "Sustainable Farming"
    ]
    
    for name in category_names:
        category = Category.objects.create(name=name)
        categories.append(category)
        print(f"Created Category: {category}")

    # Create 7 Tags
    tags = []
    tag_names = [
        "Farming", "Agriculture", "Organic", 
        "Sustainability", "Harvest", "Livestock", 
        "Crops"
    ]
    
    for name in tag_names:
        tag = Tag.objects.create(name=name)
        tags.append(tag)
        print(f"Created Tag: {tag}")

    # Create at least 7 Blogs (with more realistic data)
    blog_titles = [
        "The Future of Sustainable Agriculture",
        "Organic Farming Techniques for Beginners",
        "How Technology is Transforming Modern Farming",
        "Best Practices for Crop Rotation",
        "Raising Healthy Livestock: A Comprehensive Guide",
        "The Benefits of Organic Fertilizers",
        "Water Conservation Methods for Small Farms",
        "Urban Farming: Growing Food in Small Spaces",
        "Seasonal Planting Guide for Maximum Yield",
        "Pest Control Without Harmful Chemicals"
    ]
    
    # Get or create a test author
    author, created = User.objects.get_or_create(
        username='blogauthor',
        defaults={
            'email': 'author@example.com',
            'password': 'testpass123'
        }
    )
    
    for i, title in enumerate(blog_titles):
        blog = Blog.objects.create(
            title=title,
            content=f"""
            <h1>{title}</h1>
            <p>This is a detailed blog post about {title.lower()}.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
            Nullam auctor, nisl eget ultricies tincidunt, nisl nisl aliquam nisl, 
            eget ultricies nisl nisl eget nisl. Nullam auctor, nisl eget ultricies 
            tincidunt, nisl nisl aliquam nisl, eget ultricies nisl nisl eget nisl.</p>
            <p>More content about {title.lower()} would go here...</p>
            """,
            author=author,
            category=random.choice(categories) if i % 2 == 0 else None  # Some with, some without category
        )
        # Add 2-4 random tags to each blog
        blog.tags.set(random.sample(tags, random.randint(2, 4)))
        print(f"Created Blog: {blog} (Category: {blog.category}, Tags: {list(blog.tags.all())})")

    print("\nSuccessfully created dummy blog data!")
    print(f"- Categories: {Category.objects.count()}")
    print(f"- Tags: {Tag.objects.count()}")
    print(f"- Blogs: {Blog.objects.count()}")

if __name__ == "__main__":
    create_blog_dummy_data()