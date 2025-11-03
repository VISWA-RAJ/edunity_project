# games/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_home_view, name='games'),
    path('snake/', views.snake_game_view, name='snake_game'),
    path('flappy-bird/', views.flappy_bird_view, name='flappy_bird'),
    # --- ADD THE NEW DINO GAME URL ---
    path('dino/', views.dino_game_view, name='dino_game'),
    path('collector/', views.coin_collector_view, name='coin_collector'),

    path('submit-score/', views.submit_score_view, name='submit_score'),
    
    # --- THIS IS THE NEW, UPDATED URL FOR THE EXCLUSIVE GAME ---
    path('flappy-roast-politics/', views.flappy_roast_view, name='flappy_roast_politics'),

    
]

