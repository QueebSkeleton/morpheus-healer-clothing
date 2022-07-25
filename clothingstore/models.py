from django.db import models
from django.contrib.auth import models as auth_models


class Category(models.Model):
    """
    Product category, useful for grouping and navigating products.
    """
    slug = models.SlugField(max_length=80, primary_key=True, db_index=True,
                            unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    """
    An individual designed product.
    """
    category = models.ForeignKey(to=Category, null=True,
                                 on_delete=models.SET_NULL)
    stock_keeping_unit = models.SlugField(max_length=255, db_index=True,
                                          primary_key=True)
    title = models.CharField(max_length=80)
    body = models.TextField(blank=True)
    enabled = models.BooleanField()
    units_in_stock = models.PositiveSmallIntegerField()
    unit_cost = models.DecimalField(max_digits=9, decimal_places=4)
    unit_price = models.DecimalField(max_digits=9, decimal_places=4)

    def __str__(self):
        return self.title

    def is_available(self):
        return self.units_in_stock > 0


class ProductImage(models.Model):
    """
    An image reference for a product.
    """
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image = models.ImageField()
    alternate_text = models.CharField(max_length=255)


class Order(models.Model):
    """
    Represents an order made by a customer.
    """
    placed_by = models.ForeignKey(to=auth_models.User,
                                  on_delete=models.PROTECT)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    contact_number = models.CharField(max_length=14)
    status = models.CharField(choices=(('NEW', 'New'),
                                       ('PRC', 'Processing'),
                                       ('DLV', 'Delivering'),
                                       ('FIN', 'Finished'),
                                       ('DND', 'Denied'),
                                       ('CNC', 'Cancelled')),
                              max_length=3)
    delivery_fee = models.DecimalField(max_digits=9, decimal_places=4)
    placed_on = models.DateTimeField(auto_now_add=True)
    additional_notes = models.TextField(null=True, blank=True)
    payment_details = models.TextField()

    def get_subtotal(self):
        subtotal = 0
        for orderitem in self.orderitem_set.all():
            subtotal += orderitem.get_subtotal()
        return subtotal

    def get_total(self):
        return self.get_subtotal() + self.delivery_fee


class OrderItem(models.Model):
    """
    A purchased item inside of an order.
    """
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=9, decimal_places=4)
    quantity = models.PositiveSmallIntegerField()

    def get_subtotal(self):
        return self.unit_price * self.quantity
