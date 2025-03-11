import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from core.asgi import application


@pytest.mark.asyncio
async def test_photo_consumer_progress():
    photo_id = 42
    communicator = WebsocketCommunicator(application, f"/ws/photos/{photo_id}/")
    connected, _ = await communicator.connect()
    assert connected

    # Имитируем отправку сообщения через channel_layer (как делает Celery-задача)
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"photo_{photo_id}",
        {
            "type": "photo.progress",
            "photo_id": photo_id,
            "progress": 50,
        },
    )

    # Ожидаем получения сообщения от consumer
    response = await communicator.receive_json_from(timeout=2)
    assert response["type"] == "progress"
    assert response["photo_id"] == photo_id
    assert response["progress"] == 50

    await communicator.disconnect()
