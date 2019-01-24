from django.conf.urls import url
from . import views

app_name = 'cart'


urlpatterns = [
    url(r'^cart-add/(?P<product_id>\d+)/$', views.cart_add, name='add'),
    url(r'^cart-remove/(?P<product_id>\d+)/$', views.cart_remove, name='remove'),
    url(r'^cart-detail/$', views.cart_detail, name='detail'),
    url(r'^home_cart_add/(?P<get_product_id>\d+)/$', views.home_add, name='home'),
]
