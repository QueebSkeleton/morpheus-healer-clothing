from copy import copy

from django.conf import settings
from django.db.models import Count

from .models import Product

def cart(request):
    cart = copy(request.session.get('cart', {}))
    
    # Sum all quantities
    total_qty = 0
    for qty in cart.values():
        total_qty += qty

    # Fetch the product + images from the database
    products_in_cart = Product.objects.filter(pk__in=cart.keys()) \
                                      .prefetch_related('productimage_set') \
                                      .annotate(productimage_count=Count('productimage'))
    
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
    
    return {'shopping_cart': {'cart': cart, 'delivery_fee': settings.DELIVERY_FEE,
                              'total_qty': total_qty, 'subtotal': subtotal,
                              'total': subtotal + settings.DELIVERY_FEE}}
