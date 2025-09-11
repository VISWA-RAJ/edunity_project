# studymaterials/models.py
from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    uploaded_file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # This part sets the default ordering for all queries
    class Meta:
        ordering = ['-uploaded_at']


# studymaterials/models.py (add at the end)
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile # Import the Profile model

@receiver(post_save, sender=Material)
def award_points_for_material(sender, instance, created, **kwargs):
    if created: # Only award points when a new material is created
        try:
            profile = instance.uploader.profile
            profile.points += 20
            profile.save()
        except Profile.DoesNotExist:
            pass # Fails silently if a profile somehow doesn't exist