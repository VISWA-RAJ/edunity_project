# lostandfound/models.py
from django.db import models
from django.contrib.auth.models import User

class LostItem(models.Model):
    STATUS_CHOICES = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    item_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    last_known_location = models.CharField(max_length=200, blank=True)
    contact_info = models.CharField(max_length=200, help_text="Enter your phone number or email.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Lost')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ['-reported_at']

# lostandfound/models.py (add at the end)

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile # Import the Profile model to add points

@receiver(post_save, sender=LostItem)
def award_points_for_lost_item(sender, instance, created, **kwargs):
    """
    Awards 15 points to a user when they report a new lost item.
    """
    if created: # This ensures points are only given once
        try:
            profile = instance.reported_by.profile
            profile.points += 15
            profile.save()
        except Profile.DoesNotExist:
            pass # Fails silently if a profile somehow doesn't exist