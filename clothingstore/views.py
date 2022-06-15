from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Count

from .models import Product

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('clothingstore:store'))

def store(request):
    # TODO: get a category if it exists

    product_list = Product.objects.all().prefetch_related('productimage_set') \
                                        .annotate(image_count=Count('productimage'))
    return render(request, 'clothingstore/store.html', {'product_list': product_list})
