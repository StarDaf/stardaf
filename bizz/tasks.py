from celery import task
from django.core.mail import send_mail
from .models import Shop
from django.shortcuts import get_object_or_404


@task
def shop_created(shop_id):

    # get shop
    shop = get_object_or_404(Shop, id=shop_id)
    subject = '{}\'s business is online!!'.format(shop.user.username)
    message = 'Congratulations {}, You can add products to your shop through your profile'.format(shop.user.username)

    send_mail(subject, message, 'postmaster@stardaf.com', [shop.user.email], fail_silently=False)

    return send_mail
