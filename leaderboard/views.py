# leaderboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Profile

@login_required
def leaderboard_home_view(request):
    """
    Fetches the top 4 profiles and the current user's specific rank.
    """
    # Get all profiles, ordered by points. This is the full ranking.
    all_profiles = Profile.objects.order_by('-points')
    
    # Get the top 4 profiles from that list for the main display
    top_profiles = all_profiles[:4]
    
    # --- Find the current user's rank ---
    current_user_rank = None
    current_user_profile = request.user.profile
    
    # --- THIS IS THE CORRECTED, HIGH-PERFORMANCE LOGIC ---
    try:
        # Count how many profiles have *more* points than the current user.
        # That number + 1 is their rank. This is a fast, indexed query.
        current_user_rank = Profile.objects.filter(points__gt=current_user_profile.points).count() + 1
    except Exception:
        # This handles any failsafe case
        current_user_rank = "N/A"
        
    context = {
        'top_profiles': top_profiles,
        'current_user_rank': current_user_rank,
        'current_user_profile': current_user_profile,
    }
    return render(request, 'leaderboard/leaderboard.html', context)