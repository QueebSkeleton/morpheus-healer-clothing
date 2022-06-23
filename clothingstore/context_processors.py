from copy import copy

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
    for item in cart.items():
        for product in products_in_cart:
            sku = product.stock_keeping_unit
            if sku == item[0]:
                cart[sku] = {'product': product,
                             'quantity': item[1]}
                break
    
    return {'cart': cart, 'cart_total_qty': total_qty}
