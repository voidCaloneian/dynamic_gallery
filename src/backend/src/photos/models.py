from django.db import models

STATUS_CHOICES = (
    ("uploaded", "Uploaded"),
    ("processing", "Processing"),
    ("processed", "Processed"),
    ("failed", "Failed"),
)


class Photo(models.Model):
    image = models.ImageField(upload_to=".")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="uploaded")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.pk} - {self.status}"
