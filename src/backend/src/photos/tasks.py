import time
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist
from .models import Photo


@shared_task
def process_photo_task(photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)  # pylint: disable=no-member
    except ObjectDoesNotExist:
        return

    channel_layer = get_channel_layer()
    group_name = f"photo_{photo_id}"

    # Симуляция обработки фото
    try:
        for progress in range(0, 101, 20):
            # отправляем прогресс по WebSocket
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    "type": "photo_progress",  # изменено с photo.progress
                    "progress": progress,
                    "photo_id": photo_id,
                },
            )
            time.sleep(1)  # имитация длительного процесса

        photo.status = "processed"
        photo.save()

        # уведомление об окончании обработки
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "photo_completed",  # изменено с photo.completed
                "status": "processed",
                "photo_id": photo_id,
            },
        )
    except Exception as e:  # pylint: disable=broad-except
        photo.status = "failed"
        photo.save()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "photo_failed",  # изменено с photo.failed
                "error": str(e),
                "photo_id": photo_id,
            },
        )
