from . import models

from django.conf import settings
from django.db.models import Count

from copy import copy


def cart(request):
    """
    Places a shopping cart object in the context.
    TODO: Might be expensive as a context processor with regards to:
        - Fetching the products from the database
    """
    cart = copy(request.session.get('cart', {}))

    # Sum all quantities
    total_qty = 0
    for qty in cart.values():
        total_qty += qty

    # Fetch the product + images from the database
    products_in_cart = (models.Product.objects.filter(pk__in=cart.keys())
                              .prefetch_related('productimage_set')
                              .annotate(productimage_count=Count(
                                  'productimage')))

    # Add the associated products into the cart copy
    subtotal = 0
    for item in cart.items():
        for product in products_in_cart:
            sku = product.stock_keeping_unit
            if sku == item[0]:
                cart[sku] = {'product': product,
                             'quantity': item[1],
                             'subtotal': product.unit_price * item[1]}
                subtotal += cart[sku]['subtotal']
                break

    return {'shopping_cart': {'cart': cart,
                              'delivery_fee': settings.DELIVERY_FEE,
                              'total_qty': total_qty, 'subtotal': subtotal,
                              'total': subtotal + settings.DELIVERY_FEE}}
