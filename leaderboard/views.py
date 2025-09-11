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
    
    # Convert the queryset to a list to find the index (rank)
    profile_list = list(all_profiles)
    try:
        # The rank is the user's index in the list + 1
        current_user_rank = profile_list.index(current_user_profile) + 1
    except ValueError:
        # This handles the case where a user might not be in the list for some reason
        current_user_rank = "N/A"
        
    context = {
        'top_profiles': top_profiles,
        'current_user_rank': current_user_rank,
        'current_user_profile': current_user_profile,
    }
    return render(request, 'leaderboard/leaderboard.html', context)