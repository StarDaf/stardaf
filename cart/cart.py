from decimal import Decimal
from django.conf import settings
from bizz.models import Product

class Cart(object):

    def __init__(self, request):

        self.session = request.session # get current session

        # check if their is a cart in session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # set cart in the session as an empty dictionary
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart


    def add(self, product, quantity=1, update_quantity=False):
        """adding product to the cart."""

        # get product id
        product_id = str(product.id)

        # check if id is in dictionary
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                'price' : str(product.price),
                'quantity' : 0,
            }

        if update_quantity == True:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()  # save to session.

    def remove(self, product):
        '''removing products from the cart.'''
        product_id = str(product.id)

        if self.cart.get(product_id):
            del self.cart[product_id]
            self.save()


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def __iter__(self):

        product_ids = self.cart.keys()  # get keys of items in the cart
        products = Product.objects.filter(id__in=product_ids)  # get the products that have same ids as keys

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        # save cart items to session
        self.session[settings.CART_SESSION_ID] = self.cart
        # show that cart has being modified
        self.session.modified = True


