# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/', views.my_profile_view, name='my_profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    
    # --- NEW URL FOR POINT CONVERSION ---
    path('profile/convert/', views.convert_points_view, name='convert_points'),
    
    path('users/', views.user_list_view, name='user_list'),
    path('user/<str:username>/', views.view_user_profile_view, name='view_user_profile'),
    
    path('friend-request/send/<str:username>/', views.send_friend_request_view, name='send_friend_request'),
    path('friend-request/accept/<int:request_id>/', views.accept_friend_request_view, name='accept_friend_request'),
    path('friend-request/decline/<int:request_id>/', views.decline_friend_request_view, name='decline_friend_request'),
    
    # --- THIS IS THE NEW URL FOR UNFRIENDING ---
    path('unfriend/<str:username>/', views.unfriend_view, name='unfriend'),
    
    path('notification/dismiss/<int:notification_id>/', views.dismiss_notification_view, name='dismiss_notification'),
    
    # --- THIS IS THE NEW "CLEAR ALL" URL ---
    path('notifications/clear-all/', views.clear_all_notifications_view, name='clear_all_notifications'),

    path('about/', views.about_us_view, name='about_us'),

    
]
