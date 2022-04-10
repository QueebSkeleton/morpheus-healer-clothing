from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Product

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('clothingstore:store'))

def store(request):
    # TODO: get a category if it exists

    product_list = Product.objects.all().prefetch_related('variant_set')
    return render(request, 'clothingstore/store.html', {'product_list': product_list})
