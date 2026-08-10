
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.user.models import UserProfile
from apps.project.models import Organization  

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        org, _ = Organization.objects.get_or_create(name="Default Organization")
        UserProfile.objects.create(user=instance, organization=org)

