from django import forms


class AddToCartForm(forms.Form):

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
