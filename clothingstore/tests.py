import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Product

# Create your tests here.


class ProductTestCase(TestCase):
    def is_recent_with_one_week_ago(self):
        """
        Normal case for recent products.
        """
        recent_product = Product(created_on=timezone.now()
                                 - datetime.timedelta(days=6, hours=23, minutes=59))
        recent_product.save()
        self.assertEquals(recent_product.is_recent(), True)

    def is_recent_with_more_than_one_week_ago(self):
        """
        Case for products created more than a week ago.
        """
        past_product = Product(created_on=timezone.now()
                               - datetime.timedelta(days=7))
        past_product.save()
        self.assertEquals(past_product.is_recent(), False)

    def is_recent_with_future(self):
        """
        Case for products created in the future(?)
        """
        future_product = Product(created_on=timezone.now()
                                 + datetime.timedelta(seconds=1))
        future_product.save()
        self.assertEquals(future_product.is_recent(), False)
