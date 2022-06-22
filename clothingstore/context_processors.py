
def cart(self, request):
    return {'cart': request.session['cart']}
