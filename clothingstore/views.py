from . import forms
from . import models

import io
import os

from django.conf import settings
from django.contrib.auth import decorators as auth_decorators
from django.db import models as db_models
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.urls import reverse

from pyinvoice import models as pyinvoice_models
from pyinvoice import templates as pyinvoice_templates


def index(request):
    """
    Home page.
    """
    top_product_list = (models.Product.objects.all()
                              .prefetch_related('productimage_set')
                              .annotate(image_count=db_models
                                        .Count('productimage'))[:4])
    return render(request, 'clothingstore/index.html',
                  {'top_product_list': top_product_list})


def store(request, category_slug=None):
    """
    Main store page.
    """
    category_list = models.Category.objects.all()
    # Fetch all products
    product_list = (models.Product.objects.all()
                          .prefetch_related('productimage_set')
                          .annotate(image_count=db_models
                                    .Count('productimage')))
    # Filter by category, if category is given
    if category_slug:
        category = models.Category.objects.get(pk=category_slug)
        product_list = product_list.filter(category=category)

    return render(request, 'clothingstore/store.html',
                  {'product_list': product_list,
                   'category_list': category_list})


def add_to_cart(request, product_stock_keeping_unit):
    """
    View for adding a product to cart.
    """
    product = (models.Product.objects
                     .prefetch_related('productimage_set')
                     .annotate(image_count=db_models.Count('productimage'))
                     .get(pk=product_stock_keeping_unit))

    if request.method == 'POST':
        form = forms.AddToCartForm(request.POST, product=product)

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
        form = forms.AddToCartForm(initial=initial_data, product=product)

    return render(request, 'clothingstore/add_to_cart.html',
                  {'form': form, 'product': product})


def remove_from_cart(request, product_stock_keeping_unit):
    """
    View for removing an item from the cart.
    """
    cart = request.session['cart']
    del cart[product_stock_keeping_unit]
    request.session['cart'] = cart
    # Redirect back to cart
    return HttpResponseRedirect(reverse('clothingstore:cart'))


def remove_all_from_cart(request):
    """
    View for removing all items from cart
    """
    del request.session['cart']
    return HttpResponseRedirect(reverse('clothingstore:cart'))


def cart(request):
    """
    User shopping cart page.
    """
    return render(request, 'clothingstore/cart.html', {})


def about(request):
    """
    Store's about page.
    """
    return render(request, 'clothingstore/about.html', {})


@auth_decorators.login_required
def checkout(request):
    """
    View for checking out and placing an order.
    """
    if request.method == 'POST':
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():
            order = form.instance
            form_data = form.cleaned_data

            # Add order details
            order.placed_by = request.user
            order.status = 'NEW'
            order.delivery_fee = settings.DELIVERY_FEE
            # Construct billing and shipping addresses
            order.billing_address = ('%s %s%s%s%s%s%s%s %s'
                                     % (request.user.first_name,
                                        request.user.last_name,
                                        os.linesep,
                                        form_data['billing_street'],
                                        os.linesep,
                                        form_data['billing_city'],
                                        os.linesep,
                                        form_data['billing_zip'],
                                        form_data['billing_region']))
            order.shipping_address = ('%s %s%s%s%s%s%s%s %s'
                                      % (request.user.first_name,
                                         request.user.last_name,
                                         os.linesep,
                                         form_data['shipping_street'],
                                         os.linesep,
                                         form_data['shipping_city'],
                                         os.linesep,
                                         form_data['shipping_zip'],
                                         form_data['shipping_region']))
            order.save()
            # Construct items from shopping cart
            cart = request.session['cart']
            for product_sku in cart:
                product = models.Product.objects.get(pk=product_sku)
                order_item = models.OrderItem(order=order, product=product,
                                              unit_price=product.unit_price,
                                              quantity=cart[product_sku])
                order_item.save()
                # Deduct items
                product.units_in_stock -= order_item.quantity
                product.save()
            # Remove cart from session
            del request.session['cart']
            # Redirect to thank you page
            return HttpResponseRedirect(reverse('clothingstore:thank_you'))

    else:
        form = forms.CheckoutForm({'payment_details': 'Cash-on-Delivery'})

    return render(request, 'clothingstore/checkout.html', {'form': form})


def thank_you(request):
    """
    Thank you page.
    """
    return render(request, 'clothingstore/thank_you.html', {})


@auth_decorators.login_required
def profile_change(request):
    if request.method == 'POST':
        form = forms.ProfileChangeForm(request.POST)

        if form.is_valid():
            # Reconcile input with current user's details then save
            form_data = form.cleaned_data
            user = request.user
            user.first_name = form_data['first_name']
            user.last_name = form_data['last_name']
            user.email = form_data['email']

            user.save()

            return HttpResponseRedirect(
                reverse('clothingstore:profile_change'))

    else:
        form = forms.ProfileChangeForm(instance=request.user)

    return render(request, 'clothingstore/profile_change.html',
                  {'form': form})


@auth_decorators.login_required
def order_history(request):
    # Fetch orders made by current logged in user
    orders_made_by_user = (models.Order.objects.filter(placed_by=request.user)
                                 .order_by('-id'))
    return render(request, 'clothingstore/order_history.html',
                  {'order_list': orders_made_by_user})


@auth_decorators.login_required
def order_details(request, order_id):
    items = models.OrderItem.objects.select_related('product')
    order = (models.Order.objects.filter(pk=order_id)
                   .prefetch_related(db_models.Prefetch(
                       'orderitem_set', queryset=items))[0])
    return render(request, 'clothingstore/order_details.html',
                  {'order': order})


@auth_decorators.login_required
def invoice(request, order_id):
    # Fetch the order
    items = models.OrderItem.objects.select_related('product')
    order = (models.Order.objects.filter(pk=order_id)
                   .select_related('placed_by')
                   .prefetch_related(db_models.Prefetch(
                       'orderitem_set', queryset=items))[0])
    
    buffer = io.BytesIO()

    doc = pyinvoice_templates.SimpleInvoice(buffer)
    # Invoice Headers
    doc.invoice_info = pyinvoice_models.InvoiceInfo(
        order_id, order.placed_on)
    # Invoice Provider Information
    doc.service_provider_info = pyinvoice_models.ServiceProviderInfo(
        name='Morpheus Healer Clothing Store',
        street='4 Natib Street, Brgy. Barangka',
        city='Mandaluyong City',
        country='Philippines',
        post_code='1550')
    # Invoice Client Information
    billing_address = order.billing_address.split(os.linesep)
    billing_cityinfo = billing_address[3].split(' ')
    doc.client_info = pyinvoice_models.ClientInfo(
        name='%s %s' % (order.placed_by.first_name, order.placed_by.last_name),
        email=order.placed_by.email, street=billing_address[1],
        post_code=billing_cityinfo[0], city=billing_cityinfo[1],
        country='Philippines')
    # Invoice items
    for order_item in order.orderitem_set.all():
        doc.add_item(pyinvoice_models.Item(
            order_item.product.title, '',
            order_item.quantity,
            '%.2f' % order_item.unit_price))
    doc.add_item(pyinvoice_models.Item(
            'Delivery Fee', '',
            1, '%.2f' % order.delivery_fee))
    doc.finish()

    buffer.seek(0)
    return FileResponse(buffer, filename='invoice_%d.pdf' % order.id)
