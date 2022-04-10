import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Product

# Create your tests here.


class ProductTestCase(TestCase):
    def test_is_recent_with_one_week_ago(self):
        """
        Normal case for recent products.
        """
        recent_product = Product(slug="test",
                                 name="test",
                                 description="test description",
                                 enabled=True,
                                 created_on=timezone.now()
                                 - datetime.timedelta(days=6, hours=23, minutes=59))
        self.assertEquals(recent_product.is_recent(), True)

    def test_is_recent_with_more_than_one_week_ago(self):
        """
        Case for products created more than a week ago.
        """
        past_product = Product(slug="test",
                               name="test",
                               description="test description",
                               enabled=True,
                               created_on=timezone.now()
                               - datetime.timedelta(days=7, minutes=1))
        self.assertEquals(past_product.is_recent(), False)

    def test_is_recent_with_future(self):
        """
        Case for products created in the future
        """
        future_product = Product(slug="test",
                                 name="test",
                                 description="test description",
                                 enabled=True,
                                 created_on=timezone.now()
                                 + datetime.timedelta(days=1))
        self.assertEquals(future_product.is_recent(), False)
