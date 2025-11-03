# forum/models.py
from django.db import models
from django.contrib.auth.models import User

# --- Your existing models (no changes needed here) ---

class Doubt(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # --- THE CHANGE IS HERE ---
    # We've removed 'video_url' and added 'image'
    image = models.ImageField(upload_to='doubt_images/', blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Reply(models.Model):
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- NEW FIELDS FOR VOTING ---
    # We store the users who have voted to prevent them from voting multiple times.
    upvotes = models.ManyToManyField(User, related_name='reply_upvotes', blank=True)
    downvotes = models.ManyToManyField(User, related_name='reply_downvotes', blank=True)

    def __str__(self):
        return f'Reply by {self.author.username} on "{self.doubt.title}"'

    # NEW: A helper function to easily calculate the total score
    def total_votes(self):
        return self.upvotes.count() - self.downvotes.count()

    class Meta:
        ordering = ['created_at']


# --- GAMIFICATION LOGIC FOR THE FORUM ---

# --- 1. IMPORT THE M2M_CHANGED SIGNAL ---
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from core.models import Profile # Import the Profile model to add points

# --- NEW GAMIFICATION LOGIC FOR UPVOTES ---
def user_upvoted_reply(sender, instance, action, pk_set, **kwargs):
    """
    Awards +1 point to the reply author when their reply is upvoted.
    """
    if action == 'post_add': # Fires after a user is added to the 'upvotes' list
        reply_author_profile = instance.author.profile

        # --- 2. ADD THIS FIX to prevent self-voting for points ---
        # pk_set contains the ID of the user who was just added.
        user_who_voted_id = list(pk_set)[0]
        
        # Only award points if the voter is NOT the author
        if reply_author_profile.user.id != user_who_voted_id:
            reply_author_profile.points += 1
            reply_author_profile.save()


# --- 3. CONNECT THE SIGNAL (This is the main fix) ---
# This line "wires up" the function to the upvotes field.
m2m_changed.connect(user_upvoted_reply, sender=Reply.upvotes.through)


@receiver(post_save, sender=Doubt)
def award_points_for_doubt(sender, instance, created, **kwargs):
    """
    Awards 15 points to a user when they post a new doubt.
    """
    if created: # This ensures points are only given once, on creation
        try:
            profile = instance.author.profile
            profile.points += 15
            profile.save()
        except Profile.DoesNotExist:
            # Fails silently if a profile somehow doesn't exist
            pass

@receiver(post_save, sender=Reply)
def award_points_for_reply(sender, instance, created, **kwargs):
    """
    Awards 5 points to a user when they post a new reply.
    """
    if created:
        try:
            profile = instance.author.profile
            profile.points += 5
            profile.save()
        except Profile.DoesNotExist:
            pass


from django.urls import reverse

@receiver(post_save, sender=Reply)
def send_reply_notification(sender, instance, created, **kwargs):
    """
    Sends a notification to the author of a doubt when someone replies to it.
    """
    if created:
        doubt_author = instance.doubt.author
        reply_author = instance.author

        # Don't send a notification if you reply to your own doubt
        if doubt_author != reply_author:
            from core.models import Notification
            
            # The URL for the doubt detail page
            link = reverse('doubt_detail', args=[instance.doubt.id])

            Notification.objects.create(
                recipient=doubt_author,
                sender=reply_author,
                message=f'"{reply_author.username}" replied to your doubt: "{instance.doubt.title}"',
                link=link
            )