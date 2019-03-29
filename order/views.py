from django.shortcuts import render, get_object_or_404, HttpResponse
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib import messages
from .tasks import order_faisal_created
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from bizz.models import Product
from order.forms import OrderCreateForm
from coupon.models import Coupon
from django.utils import timezone

from django.http import HttpResponse
from django.views.generic import View
from order.utils import render_to_pdf #created in step 4
from django.template.loader import get_template
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa





@login_required
def order_create(request, id=None):

    # get cart  from session
    #cart = Cart(request)
    product = get_object_or_404(Product, id=id, available=True)

    if request.method == 'POST':
        form = OrderCreateForm(data=request.POST)  # prepopulate form with data.

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # the current user in the session.
            order.product = product
            order.full_name = str(request.user.get_full_name())
            order.email = str(request.user.email)
            order.save()
            quantity = 1
                
            if quantity > product.stock:
                return HttpResponse('There are only "{}" {}\'s remaining, change the quantity of your purchase and try again. thank you'.format(stock, item['product'].name))
                
            remaining = product.stock - quantity
            product.stock = remaining
            price = product.price
            product.save()
            OrderItem.objects.create(order=order, quantity=order.quantity, price=price, product=order.product)
            

            #order_faisal_created.delay(order.id)
            # create subject, message
            subject = '{}, Your stardaf order id is: {}'.format(order.user.username, order.id)
            message = '{}, Your product is coming to you. Your order is complete. \n A pdf containing your order details is attached with this email.\n Thank you \nTeam StarDaf '.format(order.user.username)
            # send_mail(subject, message, 'postmaster@stardaf.com', [order.email])
            # send_mail(subject, message, 'postmaster@stardaf.com', ['teamstardaf@gmail.com'])
            template = get_template('invoice.html')
            context = {
                    'order':order
                }
            html = template.render(context)
            #pdf = render_to_pdf('invoice.html', context)  # how to convert a HttpResponse object to bytes like object
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
            email = EmailMessage(subject, message, 'postmaster@stardaf.com', ['teamstardaf@gmail.com', order.email])
            #out = BytesIO(pdf)

            email.attach('order_{}.pdf'.format(order.id), result.getvalue(), 'application/pdf')
            email.send()


            #cart.clear()  #empty cart
            messages.success(request, 'Order has being placed successfully.')
            messages.success(request, 'Your Cart have being emptyied.')

            return render(request,
                          'order_created.html',
                          {'order':order})

    else:
        form = OrderCreateForm()
        #messages.info(request, 'You pay when your product arrives :-)')
        quantity = 1


    return render(request,
                  'order.html',
                  {'product':product,
                   'form':form,
                   'quantity':quantity})


@login_required
def order_created(request):
    
    cart = Cart(request)
    return render(request,
            'order.html',
            {'cart':cart})
            
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


@login_required
def buy(request, product_id):
    
    if request.method == 'GET':
        form = OrderCreateForm(data=request.GET)

        if form.is_valid():
            product = get_object_or_404(Product, id=product_id)
            user = request.user  # current user in the session
            print(user)
            order = form.save(commit=False)
            order.user = request.user  # the current user in the session.
            order.product = product
            order.full_name = str(request.user.get_full_name())
            order.email = str(request.user.email)
            price = product.price * int(order.quantity)
            if order.discount_code:
                now = timezone.now().today()
                try:
                    coupon = Coupon.objects.get(code=order.discount_code,
                                                    active=True,
                                                    product=order.product)
                except:
                       return HttpResponse('The discount code you used is expired. get a new one from the seller. and make sure you use it on the day he gave you.')                                 
                else:
                    price = price - (int(coupon.discount) * int(order.quantity)) 

            order.save()
            if int(order.quantity) > product.stock:
                return HttpResponse('There are only "{}" {}\'s remaining, change the quantity of your purchase and try again. thank you'.format(product.stock, product.name))

            OrderItem.objects.create(order=order, quantity=order.quantity, price=price, product=order.product)

            return render(request,
                        'buy.html',
                        {'product':product,
                        'order':order,
                        'user':user,
                        'price':price})
        else:
            print(form.errors)
            return HttpResponse('da matsala fah')                