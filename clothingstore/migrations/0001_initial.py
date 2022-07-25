# Generated by Django 4.0.6 on 2022-07-25 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('slug', models.SlugField(max_length=80, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_address', models.TextField()),
                ('shipping_address', models.TextField()),
                ('contact_number', models.CharField(max_length=14)),
                ('status', models.CharField(choices=[('NEW', 'New'), ('PRC', 'Processing'), ('DLV', 'Delivering'), ('FIN', 'Finished'), ('DND', 'Denied'), ('CNC', 'Cancelled')], max_length=3)),
                ('delivery_fee', models.DecimalField(decimal_places=4, max_digits=9)),
                ('placed_on', models.DateTimeField(auto_now_add=True)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('payment_details', models.TextField()),
                ('placed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('stock_keeping_unit', models.SlugField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField(blank=True)),
                ('enabled', models.BooleanField()),
                ('units_in_stock', models.PositiveSmallIntegerField()),
                ('unit_cost', models.DecimalField(decimal_places=4, max_digits=9)),
                ('unit_price', models.DecimalField(decimal_places=4, max_digits=9)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clothingstore.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('alternate_text', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothingstore.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=4, max_digits=9)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clothingstore.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clothingstore.product')),
            ],
        ),
    ]
