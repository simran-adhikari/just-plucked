# Generated by Django 5.2 on 2025-04-26 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Product Name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Product Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Product Image')),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Regular Price')),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Discounted Price')),
                ('stock_quantity', models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')),
                ('shelf_life_remaining', models.PositiveIntegerField(help_text='Remaining shelf life in days', verbose_name='Remaining Shelf Life (in days)')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('farmer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='farmer.farmer')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_quantity', models.PositiveIntegerField(default=0, verbose_name='Stock Quantity')),
                ('shelf_life_remaining', models.PositiveIntegerField(help_text='Remaining shelf life in days', verbose_name='Remaining Shelf Life (in days)')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='product_images/', verbose_name='Product Image')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Alt Text')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='ProductPricingHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Old Price')),
                ('new_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='New Price')),
                ('change_date', models.DateTimeField(auto_now_add=True, verbose_name='Change Date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricing_history', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Pricing History',
                'verbose_name_plural': 'Product Pricing History',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=255, verbose_name='User')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Rating')),
                ('review', models.TextField(blank=True, null=True, verbose_name='Review')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Review',
                'verbose_name_plural': 'Product Reviews',
            },
        ),
    ]
