from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from uuid import uuid4

def validate_image_size(image):
    if image.size > settings.MAX_PROFILE_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError("Image too large!")

class Account(AbstractUser):
    current_profile = models.UUIDField(null=True, blank=True, unique=True)

class Profile(models.Model):
    # A user can have multiple profiles he can use seperately for
    # relating with other entities (profiles).
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=400)
    pimg = models.ImageField(upload_to='pIMG/', validators=[validate_image_size])

