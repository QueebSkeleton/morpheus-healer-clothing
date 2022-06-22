
class CartMiddleware:
    """
    Middleware that always places a cart dictionary
    on the session.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Initialize the cart
        if not request.session.get('cart'):
            request.session['cart'] = {}
        response = self.get_response(request)
        return response
