from django.db import models
from account.models import Profile
from uuid import uuid4

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)

class Entry(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=100*1000, null=True, blank=True)

