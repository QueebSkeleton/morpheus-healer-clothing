import datetime

from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Product category, useful for grouping and navigating products.
    """
    slug = models.SlugField(max_length=80, db_index=True, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    """
    An individual designed product. Has variants.
    """
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(max_length=80, db_index=True, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    enabled = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def is_recent(self):
        """
        Checks if this product is created in the last week.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.created_on <= now


class Variant(models.Model):
    """
    Variant of a product design. Contains its own inventory information.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField()
    stock_keeping_unit = models.SlugField(
        max_length=255, db_index=True, unique=True)
    unit_cost = models.DecimalField(max_digits=7, decimal_places=2)
    units_in_stock = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Order(models.Model):
    pass


class OrderItem(models.Model):
    pass
