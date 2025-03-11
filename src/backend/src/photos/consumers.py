import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PhotoConsumer(AsyncWebsocketConsumer):
    """
    Консюмер для обработки фото Вебсокета
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photo_id = None
        self.group_name = None

    async def connect(self):
        """
        Подключение к каналу
        """
        self.photo_id = self.scope["url_route"]["kwargs"]["photo_id"]
        self.group_name = f"photo_{self.photo_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Обработчик сообщений о прогрессе
    async def photo_progress(self, event):
        """
        Обработчик сообщений о прогрессе
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": "progress",
                    "photo_id": event["photo_id"],
                    "progress": event["progress"],
                }
            )
        )

    async def photo_completed(self, event):
        """
        Обработчик сообщений об окончании обработки
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": "completed",
                    "photo_id": event["photo_id"],
                    "status": event["status"],
                }
            )
        )

    async def photo_failed(self, event):
        """
        Обработчик сообщений о неудаче
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": "failed",
                    "photo_id": event["photo_id"],
                    "error": event["error"],
                }
            )
        )
