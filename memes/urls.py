# memes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.memes_home_view, name='memes'),
    path('gallery/', views.meme_gallery_view, name='meme_gallery'),
    path('<int:meme_id>/', views.meme_detail_view, name='meme_detail'),
    path('<int:meme_id>/like/', views.like_meme_view, name='like_meme'),
    path('post/image/', views.post_image_meme_view, name='post_image_meme'),
    path('post/video/', views.post_video_meme_view, name='post_video_meme'),
]