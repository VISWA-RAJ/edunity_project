# games/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import GameScore
from core.models import Profile
from django.contrib.auth.models import User
from django.db.models import Sum # We need this for calculations

# --- NEW, CORRECT HELPER FUNCTION ---
def get_game_leaderboard():
    """
    Calculates the total game score for every user and returns the top 4.
    The total score is the SUM of their high scores from all games.
    """
    # Get all users who have at least one game score
    users_with_scores = User.objects.filter(gamescore__isnull=False).distinct()
    
    # Calculate the total score for each user
    leaderboard_data = []
    for user in users_with_scores:
        total_score = GameScore.objects.filter(user=user).aggregate(total=Sum('score'))['total']
        leaderboard_data.append({'user': user, 'total_score': total_score})
        
    # Sort the users by their total score in descending order
    leaderboard_data.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Return the top 4
    return leaderboard_data[:4]

@login_required
def games_home_view(request):
    """
    Displays the main games page and the total score leaderboard.
    """
    leaderboard = get_game_leaderboard()
    context = {
        'leaderboard': leaderboard
    }
    return render(request, 'games/games.html', context)

@login_required
def tic_tac_toe_view(request):
    return render(request, 'games/tic_tac_toe.html')

@login_required
def snake_game_view(request):
    top_snake_scores = GameScore.objects.filter(game_name='Snake').order_by('-score')[:3]
    context = { 'top_snake_scores': top_snake_scores }
    return render(request, 'games/snake_game.html', context)

# --- THE NEW, CORRECTED "BRAIN" OF THE GAME MODULE ---
@csrf_exempt
@login_required
def submit_score_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        game_name = data.get('game')
        score = int(data.get('score', 0))
        user = request.user

        # 1. Get the old top 4 leaderboard BEFORE making any changes
        old_leaderboard = get_game_leaderboard()
        old_top_users = [item['user'] for item in old_leaderboard]

        # 2. Update the user's high score for this specific game
        current_score, created = GameScore.objects.get_or_create(
            user=user, 
            game_name=game_name,
            defaults={'score': 0}
        )
        if score > current_score.score:
            current_score.score = score
            current_score.save()

        # 3. Get the new top 4 leaderboard AFTER the score has been updated
        new_leaderboard = get_game_leaderboard()
        new_top_users = [item['user'] for item in new_leaderboard]
        
        # 4. Apply the complex EDUnity point adjustment logic
        rank_points = {0: 25, 1: 18, 2: 12} # Ranks 1, 2, 3 (using index 0, 1, 2)

        # First, deduct points from anyone who dropped off or changed rank
        for i, old_user in enumerate(old_top_users):
            if i < len(new_top_users) and old_user == new_top_users[i]:
                continue # User is still at the same rank, no change
            if i in rank_points:
                old_user.profile.points -= rank_points[i]
                old_user.profile.save()

        # Second, add points to anyone who is new or moved up
        for i, new_user in enumerate(new_top_users):
            if i < len(old_top_users) and new_user == old_top_users[i]:
                continue # User is still at the same rank, no change
            if i in rank_points:
                new_user.profile.points += rank_points[i]
                new_user.profile.save()

        return JsonResponse({'status': 'success', 'message': 'Score processed!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def flappy_bird_view(request):
    """
    Serves the page for the Flappy Bird game and its specific leaderboard.
    """
    top_flappy_scores = GameScore.objects.filter(game_name='Flappy Bird').order_by('-score')[:3]
    context = {
        'top_flappy_scores': top_flappy_scores
    }
    return render(request, 'games/flappy_bird.html', context)

@login_required
def dino_game_view(request):
    """
    Serves the page for the Dino Run game and its specific leaderboard.
    """
    # The score is the distance, so higher is better.
    top_dino_scores = GameScore.objects.filter(game_name='Dino Run').order_by('-score')[:3]
    
    context = {
        'top_dino_scores': top_dino_scores
    }
    return render(request, 'games/dino_game.html', context)

@login_required
def coin_collector_view(request):
    """
    Serves the page for the Coin Collector game and its specific leaderboard.
    """
    top_collector_scores = GameScore.objects.filter(game_name='Coin Collector').order_by('-score')[:3]
    
    context = {
        'top_collector_scores': top_collector_scores
    }
    return render(request, 'games/coin_collector.html', context)
