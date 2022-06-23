from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Count

from .forms import AddToCartForm
from .models import Product

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('clothingstore:store'))


def store(request):
    product_list = Product.objects.all().prefetch_related('productimage_set') \
                                        .annotate(image_count=Count('productimage'))
    return render(request, 'clothingstore/store.html', {'product_list': product_list})


def add_to_cart(request, stock_keeping_unit):
    product = Product.objects.get(pk=stock_keeping_unit)

    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)

        if form.is_valid():
            # Save to cart
            cart = request.session['cart']
            cart[product.stock_keeping_unit] = form.cleaned_data['quantity']
            request.session['cart'] = cart
            # Redirect back to store
            return HttpResponseRedirect(reverse('clothingstore:store'))

    else:
        # Get current quantity from cart if it exists
        initial_data = {'quantity': request.session['cart']
                        .get(product.stock_keeping_unit, 1)}
        form = AddToCartForm(initial=initial_data, product=product)

    return render(request, 'clothingstore/add_to_cart.html',
                  {'form': form, 'product': product})


def cart(request):
    return render(request, 'clothingstore/cart.html', {})
