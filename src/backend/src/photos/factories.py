import factory
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from photos.models import Photo


def generate_test_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(file, "PNG")
    file.name = "test.png"
    file.seek(0)
    return SimpleUploadedFile(
        name="test.png", content=file.getvalue(), content_type="image/png"
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    image = factory.LazyFunction(generate_test_image)
    status = "uploaded"
