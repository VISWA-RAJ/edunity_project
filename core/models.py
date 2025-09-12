# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="Tell us a little about yourself.")
    friends = models.ManyToManyField('self', blank=True)


    @property
    def image_url(self):
        """
        Returns the URL for the user's profile image.
        If the user has not uploaded an image, it returns the URL for the default image.
        """
        # --- THIS IS THE FINAL FIX ---
        # We explicitly check if the image field has a file associated with it.
        # This is the most robust way to handle this.
        if self.image and self.image.name:
            return self.image.url
        else:
            return static('images/profile_pics/default.jpg')
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # --- THE FIX IS HERE ---
    # This check ensures we only try to save the profile if it has been created.
    # This prevents errors and makes the code much more robust.
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Notification(models.Model):
    # The user who will receive the notification
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    # The user who triggered the notification (optional, can be null for system messages)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    # The message that will be displayed
    message = models.TextField()
    # A link to the relevant page (e.g., the doubt or lost item)
    link = models.URLField(max_length=200, blank=True)
    # Tracks if the notification has been seen
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.username}: {self.message[:30]}'

    class Meta:
        ordering = ['-timestamp'] # Show newest notifications first