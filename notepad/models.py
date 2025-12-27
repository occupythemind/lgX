from django.db import models
from account.models import Profile
from uuid import uuid4
from django.utils.timezone import now

class Topic(models.Model):
    class TopicStatus(models.TextChoices):
        active = 'ACTIVE', 'active'
        draft = 'DRAFT', 'draft'
        trash = 'TRASH', 'trash'

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    # by default, all topics made are active and not drafts; you would need specify if it's
    # a draft or not.
    status = models.CharField(max_length=6, choices=TopicStatus.choices, default='ACTIVE')
    created = models.DateTimeField(auto_now_add=True)

class Entry(models.Model):
    class EntryStatus(models.TextChoices):
        active = 'ACTIVE', 'active'
        draft = 'DRAFT', 'draft'
        trash = 'TRASH', 'trash'

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid4)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.CharField(max_length=100*1000, null=True, blank=True)
    status = models.CharField(max_length=6, choices=EntryStatus.choices, default='ACTIVE')
    created = models.DateTimeField(auto_now_add=True)


