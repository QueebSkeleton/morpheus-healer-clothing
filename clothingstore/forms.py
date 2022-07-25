from django import forms

from . import models
from django.contrib.auth import models as auth_models


class AddToCartForm(forms.Form):
    """
    Form for adding a product to the shopping cart.
    """
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.product = kwargs['product']
        del kwargs['product']
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if quantity > self.product.units_in_stock:
            raise forms.ValidationError("""
                                        Specified quantity exceeds stock.
                                        A maximum of %d is allowed.
                                        """ % self.product.units_in_stock)

        return quantity


class CheckoutForm(forms.ModelForm):
    """
    Form for checking out and placing an order.
    """
    # Billing and shipping information
    billing_street = forms.CharField(max_length=255)
    billing_city = forms.CharField(max_length=255)
    billing_zip = forms.CharField(max_length=4)
    billing_region = forms.CharField(max_length=255)
    is_shipping_same_to_billing = forms.BooleanField()
    shipping_street = forms.CharField(max_length=255)
    shipping_city = forms.CharField(max_length=255)
    shipping_zip = forms.CharField(max_length=4)
    shipping_region = forms.CharField(max_length=255)

    class Meta:
        model = models.Order
        fields = ['contact_number', 'additional_notes', 'payment_details',]


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = auth_models.User
        fields = ['first_name', 'last_name', 'email',]
