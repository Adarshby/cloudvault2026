from django.db import models
from django.contrib.auth.models import User
import uuid


class File(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='uploads/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    download_count = models.IntegerField(
        default=0
    )

    share_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    def __str__(self):
        return self.file.name


class AccessLog(models.Model):

    file = models.ForeignKey(
        File,
        on_delete=models.CASCADE
    )

    accessed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.accessed_by} accessed {self.file}"