# games/models.py
from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=50) # e.g., "Snake", "Asteroids"
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.game_name}: {self.score}'

    class Meta:
        # This ensures a user can only have one score per game (their highest)
        unique_together = ('user', 'game_name')
        ordering = ['-score']