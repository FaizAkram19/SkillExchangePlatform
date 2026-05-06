from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_a_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    