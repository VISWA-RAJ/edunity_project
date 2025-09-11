# studymaterials/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # CORRECTED: The name is now 'materials' to match the template
    path('', views.materials_home_view, name='materials'), 
    
    path('all/', views.material_list_view, name='material_list'),
    path('upload/', views.upload_material_view, name='upload_material'),
]