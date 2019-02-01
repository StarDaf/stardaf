from django.shortcuts import render, get_object_or_404, HttpResponse
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib import messages
from .tasks import order_faisal_created
from django.core.mail import send_mail

from django.http import HttpResponse
from django.views.generic import View
from order.utils import render_to_pdf #created in step 4
from django.template.loader import get_template

@login_required
def order_created(request):

    # get cart  from session
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST)  # prepopulate form with data.

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # the current user in the session.
            order.full_name = str(request.user.get_full_name())
            order.email = str(request.user.email)
            order.save()
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                stock = product.stock
                
                if quantity > stock:
                    return HttpResponse('There are only "{}" {}\'s remaining, change the quantity of your purchase and try again. thank you'.format(stock, item['product'].name))
                
                remaining = stock - quantity
                product.stock = remaining
                product.save()
                OrderItem.objects.create(order=order, quantity=item['quantity'], price=item['price'], product=item['product'])


            #order_faisal_created.delay(order.id)
            # create subject, message
            subject = '{}, Your stardaf order id is: {}'.format(order.user.username, order.id)
            message = '{}, Your product is coming to you. Your order is complete. \n A pdf containing your order details is attached with this email.\n Thank you \nTeam StarDaf '.format(order.user.username)
            send_mail(subject, message, 'postmaster@stardaf.com', [order.email])
            cart.clear()  #empty cart

            messages.success(request, 'Order has being placed successfully.')
            messages.success(request, 'Your Cart have being emptyied.')

            return render(request,
                          'order_created.html',
                          {'order':order})

    else:
        form = OrderCreateForm()
        messages.info(request, 'You pay when your product arrives :-)')


    return render(request,
                  'order.html',
                  {'cart':cart,
                   'form':form})


    
@login_required
def order_pdf(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    template = get_template('pdf/invoice.html')
    context = {
            'order':order
        }
    html = template.render(context)
    pdf = render_to_pdf('invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "%s_%s.pdf" %(str(order.user.username), str(order.id))
        content = "inline; filename='%s'" %(filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")    