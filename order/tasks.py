from celery import task
from django.core.mail import send_mail
from .models import Order
from django.shortcuts import get_object_or_404

@task
def order_faisal_created(order_id):

    # get order
    order = get_object_or_404(Order, id=order_id)

    # create subject, message
    subject = '{}, Your order_id is: {}'.format(order.user.username, order.id)
    message = '{}, Your product is coming to you.'
    send_mail(subject, message, 'teamstardaf@gmail.com', [order.email])

    return send_mail


@task
def order_faisal_created(order_id):

    # get order
    order = get_object_or_404(Order, id=order_id)

    # create subject, message
    subject = '{}, Your order_id is: {}'.format(order.user.username, order.id)
    message = '{}, Your product is coming to you.'
    send_mail(subject, message, 'teamstardaf@gmail.com', [order.email])

    return send_mail