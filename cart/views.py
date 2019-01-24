from django.shortcuts import render, redirect
from .cart import Cart
from bizz.models import Product
from django.shortcuts import get_object_or_404
from .forms import CartAddForm
from django.contrib.auth.decorators import login_required


@login_required
def cart_add(request, product_id):
    """function for adding product to cart."""

    # get cart from session
    cart = Cart(request)

    # get product
    product = get_object_or_404(Product, id=product_id)

    form = CartAddForm(data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data

        # add product to cart
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:detail')   # redirect to cart.

@login_required
def home_add(request, get_product_id):
    # get cat from session
    cart = Cart(request)

    # get product
    product = get_object_or_404(Product, id=get_product_id)

    # add to cart
    cart.add(product=product, quantity=1, update_quantity=False)

    return redirect('cart:detail')   # redirect to cart.


@login_required
def cart_remove(request, product_id):
    """function for removing product from cart."""

    cart = Cart(request)  # get cart from session
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:detail')




def cart_detail(request):

    cart = Cart(request)  # get cart

    # add a quantity form for each item in the cart
    for item in cart:
        item['cart_update_quantity_form'] = CartAddForm(initial={
            'quantity':item['quantity'],
            'update':True
        })

    return render(request,
                  'cart_detail.html',
                  {'cart':cart})



