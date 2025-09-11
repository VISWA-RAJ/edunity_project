# lostandfound/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lostandfound_home_view, name='lost_and_found'),
    path('report/', views.report_lost_view, name='report_lost'),
    path('all/', views.all_lost_items_view, name='all_lost_items'),
    # --- ADD THIS NEW URL FOR THE DETAIL PAGE ---
    path('item/<int:item_id>/', views.item_detail_view, name='item_detail'),
    path('found/<int:item_id>/', views.found_item_view, name='found_item'),
    path('delete/<int:item_id>/', views.delete_lost_item_view, name='delete_lost_item'),
]