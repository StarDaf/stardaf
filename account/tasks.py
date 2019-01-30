from celery import task
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User

@task
def account_created(user_id):
    # get user
    user = get_object_or_404(User, id=user_id)
    subject = 'Welcome {} to casbah'.format(user.get_full_name())
    message = 'Hello Dear!!, You have arrived at the first ultimate social commerce site in the world!<br//>' \
              'Where you can browse and buy cool products and also set you business online' \

    send_mail(subject, message, 'postmaster@stardaf.com', [user.email], fail_silently=False)

    return send_mail
