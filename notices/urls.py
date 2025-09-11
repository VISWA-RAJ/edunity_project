# notices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The main page that lists all notices
    path('', views.notice_list_view, name='notices'),
    # The new, separate page for posting a notice
    path('post/', views.post_notice_view, name='post_notice'),
]