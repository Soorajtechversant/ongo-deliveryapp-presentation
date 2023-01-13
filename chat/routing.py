from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('chat/<id>/', consumers.ChatConsumer.as_asgi()),

]