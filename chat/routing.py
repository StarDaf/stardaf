# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url('^/chats/ws/chat/Faisal/$', consumers.ChatConsumer),
]