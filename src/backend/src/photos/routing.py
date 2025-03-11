from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/photos/(?P<photo_id>\w+)/$", consumers.PhotoConsumer.as_asgi()),
]
