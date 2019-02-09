from django.conf.urls import url
from . import views

app_name='bizz'

urlpatterns = [
    url(r'^create-shop/(?P<user_id>\d+)/$', views.create_shop, name='create'),
    url(r'^edit-shop/$', views.edit, name='edit'),
    url(r'^add-product/(?P<shop_id>\d+)/$', views.add_product, name='add_product'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/(?P<username>[-\w]+)/$', views.detail, name='detail'),
    url(r'^(?P<product_id>\d+)/$', views.delete, name='delete'),
    url(r'^like/$', views.like, name='like'),
    url(r'^recommend/(?P<user_id>\d+)/(?P<product_id>\d+)/$', views.recommend, name='recommend'),
    url(r'update-stock/(?P<product_id>\d+)/', views.add_product_stock, name='stock'),
    #url(r'^(?P<business_name>[-\w]+)/', views.profile1, name='profile1'),
]