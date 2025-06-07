
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/votes/', consumers.VoteConsumer.as_asgi()),
]
