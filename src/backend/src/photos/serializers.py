from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Photo
    """

    class Meta:
        """
        Метаинформация о сериалайзере
        """

        model = Photo
        fields = ("id", "image", "status", "created_at")
        read_only_fields = ("status", "created_at")
