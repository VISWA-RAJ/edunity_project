# forum/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main page: /forum/
    path('', views.forum_home_view, name='forum'),
    # Ask a doubt page: /forum/ask/
    path('ask/', views.ask_doubt_view, name='ask_doubt'),
    # All doubts page: /forum/all/
    path('all/', views.doubt_list_view, name='doubt_list'),
    path('doubt/<int:doubt_id>/', views.doubt_detail_view, name='doubt_detail'),

    path('reply/<int:reply_id>/vote/', views.vote_reply_view, name='vote_reply'),
]