# polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.polls_home_view, name='polls'),
    path('create/', views.create_poll_view, name='create_poll'),
    path('<int:poll_id>/vote/', views.vote_view, name='vote'),
]