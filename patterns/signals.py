from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Favourite


@receiver(post_save, sender=User)
def create_user_favourite(sender, instance, created, **kwargs):
    if created:
        Favourite.objects.create(user=instance)
