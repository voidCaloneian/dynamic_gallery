import io
import pytest
from PIL import Image
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from photos.models import Photo
from photos.factories import PhotoFactory


@pytest.fixture
def api_client():
    return APIClient()


def create_test_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file, "PNG")
    file.name = "test.png"
    file.seek(0)
    return file


@pytest.mark.django_db
def test_photo_factory_creation():
    photo = PhotoFactory()
    assert photo.pk is not None
    assert photo.status == "uploaded"


@pytest.mark.django_db
def test_photo_upload_api(api_client):
    url = reverse("photo-list")  # URL-имя из router-а
    image_file = create_test_image()
    data = {
        "image": SimpleUploadedFile(
            name="test.png", content=image_file.read(), content_type="image/png"
        )
    }
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == 201
    photo = Photo.objects.first()
    # Вьюсет сразу меняет статус на "processing" и запускает задачу
    assert photo.status == "processing"
    assert photo.image is not None
