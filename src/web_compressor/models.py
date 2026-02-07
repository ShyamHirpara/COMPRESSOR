from django.db import models
from django.contrib.auth.models import User
import os

class CompressedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compressed_images')
    image = models.ImageField(upload_to='compressed/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    size_text = models.CharField(max_length=50)
    format = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.original_filename}"

    def delete(self, *args, **kwargs):
        # Delete the file from filesystem when model is deleted
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
