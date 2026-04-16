from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        nickname = instance.username
        slug = instance.username.lower()
        base_slug = slug
        counter = 1
        while Profile.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        Profile.objects.create(user=instance, nickname=nickname, slug=slug)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
