from .cart import Cart

def cart(request):
    return {'cart':Cart(request)}


# a cart is a python function that's takes request as an argument
# and return a dictionary that's get added to the request context.