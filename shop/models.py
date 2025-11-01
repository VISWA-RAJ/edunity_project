from django.db import models

class ShopItem(models.Model):
    # A unique ID to check for ownership in our code
    # e.g., "special-game-asteroids", "profile-theme-blue"
    unique_id = models.SlugField(max_length=100, unique=True)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(default=10) # The cost in "Edunity Tokens"

    def __str__(self):
        return f'{self.name} ({self.price} tokens)'
