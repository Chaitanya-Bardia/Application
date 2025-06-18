# myproject/routing.py

from django.urls import path
from myapp import consumers

websocket_urlpatterns = [
      # this path should match the path given in the consumer URL
    path('ws/progress/', consumers.MailProgressConsumer.as_asgi()),
]
