# edunity_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('admin/', admin.site.urls),

    # App URLs
    path('materials/', include('studymaterials.urls')),
    path('forum/', include('forum.urls')),
    path('lost-and-found/', include('lostandfound.urls')),
    path('polls/', include('polls.urls')),
    path('notices/', include('notices.urls')),
    path('memes/', include('memes.urls')),
    path('games/', include('games.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    
    # Core URLs (must be last)
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)