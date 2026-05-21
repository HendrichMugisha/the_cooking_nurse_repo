from .cart import Cart

def cart(request):
    """
    Instantiates the cart and makes it available globally 
    in all templates via the {{ cart }} variable.
    """
    return {'cart': Cart(request)}
