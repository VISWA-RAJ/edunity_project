# memes/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from core.models import Profile, Notification
from django.urls import reverse

class Meme(models.Model):
    MEME_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video Link'),
    ]
    meme_type = models.CharField(max_length=5, choices=MEME_TYPE_CHOICES)
    caption = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # These fields are now simplified
    image = models.ImageField(upload_to='memes/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    
    likes = models.ManyToManyField(User, related_name='liked_memes', blank=True)

    def __str__(self): return f'{self.get_meme_type_display()} by {self.author.username}'
    class Meta: ordering = ['-created_at']

class Comment(models.Model):
    meme = models.ForeignKey(Meme, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f'Comment by {self.author.username}'
    class Meta: ordering = ['created_at']

# --- Gamification and Notification Signals (No changes needed) ---
@receiver(post_save, sender=Meme)
def award_points_for_meme(sender, instance, created, **kwargs):
    if created:
        try:
            instance.author.profile.points += 5
            instance.author.profile.save()
        except Profile.DoesNotExist: pass

def user_liked_meme(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user_who_liked = User.objects.get(pk=list(pk_set)[0])
        try:
            user_who_liked.profile.points += 1
            user_who_liked.profile.save()
        except Profile.DoesNotExist: pass
        if instance.author != user_who_liked:
            link = reverse('meme_detail', args=[instance.id])
            Notification.objects.create(recipient=instance.author, sender=user_who_liked, message=f'"{user_who_liked.username}" liked your post.', link=link)

m2m_changed.connect(user_liked_meme, sender=Meme.likes.through)

@receiver(post_save, sender=Comment)
def award_points_for_comment(sender, instance, created, **kwargs):
    if created:
        try:
            instance.author.profile.points += 2
            instance.author.profile.save()
        except Profile.DoesNotExist: pass
        if instance.meme.author != instance.author:
            link = reverse('meme_detail', args=[instance.meme.id])
            Notification.objects.create(recipient=instance.meme.author, sender=instance.author, message=f'"{instance.author.username}" commented on your post.', link=link)