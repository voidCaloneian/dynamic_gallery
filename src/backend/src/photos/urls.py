from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PhotoViewSet

router = DefaultRouter()
router.register(r"", PhotoViewSet, basename="photo")

urlpatterns = [
    path("", include(router.urls)),
]
