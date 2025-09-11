# notices/models.py
from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    # Define the choices for the category, matching your static HTML
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('event', 'Event'),
        ('exam', 'Exam'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='general')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] # Newest notices first


# notices/models.py (add at the end)
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile # Import the Profile model

@receiver(post_save, sender=Notice)
def award_points_for_notice(sender, instance, created, **kwargs):
    if created: # Only award points for new notices
        try:
            profile = instance.author.profile
            profile.points += 10
            profile.save()
        except Profile.DoesNotExist:
            pass