from django.db.models.signals import post_save
from users.models import PersoUser, Profile
from django.dispatch import receiver


@receiver(post_save, sender=PersoUser)
def create_Profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=PersoUser)
def save_Profile(sender, instance, **kwargs):
    instance.profile.save()
