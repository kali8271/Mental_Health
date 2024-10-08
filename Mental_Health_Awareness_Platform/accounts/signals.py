from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from experts.models import Expert

@receiver(post_save, sender=UserProfile)
def create_expert_for_therapist(sender, instance, created, **kwargs):
    # Check if the user is a therapist and if an Expert entry doesn't already exist
    if created and instance.role == 'therapist':
        Expert.objects.create(
            name=instance.username,  # You can use a different name logic
            specialty="General",  # You can allow this to be updated later
            therapist=instance
        )
