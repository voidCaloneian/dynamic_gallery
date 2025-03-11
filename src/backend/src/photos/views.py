from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
from .tasks import process_photo_task


class PhotoViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Photo
    """

    queryset = Photo.objects.all().order_by("-created_at")  # pylint: disable=no-member
    serializer_class = PhotoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.save()

        # Обновляем статус и запускаем асинхронную обработку
        photo.status = "processing"
        photo.save()
        process_photo_task.delay(photo.id)

        headers = self.get_success_headers(serializer.data)
        return Response(
            PhotoSerializer(photo).data, status=status.HTTP_201_CREATED, headers=headers
        )
