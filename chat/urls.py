from django.conf.urls import url
from . import views

app_name='chat'


urlpatterns = [
    url('^mychats/$', views.chats, name='chats'),
    url('^chat/(?P<username>[-\w]+)/$', views.thread, name='thread'),
]

#url('^chat/(?P<username>[-\w]+)/(?P<product_id>\d+)/$', views.thread, name='thread'),