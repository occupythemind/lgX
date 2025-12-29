# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created(sender, instance, created, **kwargs):
    # sender -- The model that sent the action, in this case Account
    if created:
        # This runs ONLY once, when an account is created
        profile = Profile.objects.create(user=instance)
        profile.save()
        instance.current_profile_id = profile.id
        instance.save()
