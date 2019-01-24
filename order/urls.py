from django.conf.urls import url
from . import views


app_name='order'

urlpatterns = [
    url(r'^create/$', views.order_created, name='order_create'),
    url(r'^order_pdf/(?P<order_id>\d+)/$', views.order_pdf, name='pdf'),
]