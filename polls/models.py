# polls/models.py
from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # This field will track all users who have voted on this poll
    voters = models.ManyToManyField(User, related_name='voted_polls', blank=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.poll.question} - {self.text}'
    

# polls/models.py (add at the end)

from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile # Import the Profile model

@receiver(post_save, sender=Poll)
def award_points_for_poll(sender, instance, created, **kwargs):
    """
    Awards 5 points to a user when they create a new poll.
    """
    if created:
        try:
            profile = instance.created_by.profile
            profile.points += 5
            profile.save()
        except Profile.DoesNotExist:
            pass