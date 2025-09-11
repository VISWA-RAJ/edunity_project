# leaderboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard_home_view, name='leaderboard'),
]