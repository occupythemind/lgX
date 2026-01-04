from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.exceptions import ValidationError
from uuid import uuid4

def validate_image_size(image):
    if image.size > settings.MAX_PROFILE_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError("Image too large!")

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")

        email = self.normalize_email(email)  # lowercases domain + safe normalization
        user = self.model(email=email, **extra_fields)
        user.username = user.id # users can change this later on to another unique name
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
    

class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    email = models.EmailField(unique=True, max_length=254)
    current_profile_id = models.UUIDField(null=True, blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] # so username isn't required

    class Meta:
        constraints = [
            models.UniqueConstraint(
                # make sure no 2 emails are same, by converting them to lowercase and checking them
                models.functions.Lower("email"),
                name="unique_user_email_ci",
            )
    ]
    
    objects = AccountManager()
    

class Profile(models.Model):
    # A user can have multiple profiles he can use seperately for
    # relating with other entities (profiles). //Soon to write a serializer & url for //
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=300, null=True, blank=True)
    bio = models.CharField(max_length=400, null=True, blank=True)
    pimg = models.ImageField(upload_to='pIMG/', validators=[validate_image_size], null=True, blank=True)

