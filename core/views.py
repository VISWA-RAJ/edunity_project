# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, FriendRequest, Notification
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

# --- Main Page Views ---
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# --- Auth Views ---
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

# --- Profile & Friends System Views ---
@login_required
def my_profile_view(request):
    profile = request.user.profile
    friends = profile.friends.all()
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    all_notifications = Notification.objects.filter(recipient=request.user)
    
    points = profile.points
    rank = "Newcomer"
    if points >= 100: rank = "Campus Expert"
    elif points >= 50: rank = "Contributor"
    elif points >= 10: rank = "Active Member"

    context = {
        'profile': profile, 'rank': rank, 'friends': friends,
        'friend_requests': friend_requests, 'notifications': all_notifications,
    }
    return render(request, 'profile/profile.html', context)

@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('my_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/update_profile.html', {'form': form})

# core/views.py

@login_required
def user_list_view(request):
    """
    Displays a list of users ONLY if a search query is provided.
    Otherwise, it shows an empty list.
    """
    # Get the search query from the URL (?q=...)
    query = request.GET.get('q')
    users = None # Start with no users

    if query:
        # If a search term was provided, then we find matching users
        users = User.objects.filter(username__icontains=query).exclude(username=request.user.username)

    context = {
        'users': users,
        'query': query, # Pass the query back to the template
    }
    return render(request, 'profile/user_list.html', context)

@login_required
def view_user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    is_friend = request.user.profile.friends.filter(id=profile.id).exists()
    
    friends_of_viewed_user = []
    if is_friend:
        friends_of_viewed_user = profile.friends.all()

    request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user).exists()
    request_received = FriendRequest.objects.filter(from_user=user, to_user=request.user).exists()
    
    points = profile.points
    rank = "Newcomer"
    if points >= 100: rank = "Campus Expert"
    elif points >= 50: rank = "Contributor"
    elif points >= 10: rank = "Active Member"

    context = {
        'profile': profile, 'rank': rank, 'is_friend': is_friend,
        'friends_of_viewed_user': friends_of_viewed_user,
        'request_sent': request_sent, 'request_received': request_received,
    }
    return render(request, 'profile/view_user_profile.html', context)

# --- Friend and Notification Action Views ---
@login_required
def send_friend_request_view(request, username):
    if request.method == 'POST':
        to_user = get_object_or_404(User, username=username)
        if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists() and not FriendRequest.objects.filter(from_user=to_user, to_user=request.user).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('view_user_profile', username=username)

@login_required
def accept_friend_request_view(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        from_user_profile = friend_request.from_user.profile
        to_user_profile = request.user.profile
        to_user_profile.friends.add(from_user_profile)
        from_user_profile.friends.add(to_user_profile)
        friend_request.delete()
    return redirect('my_profile')

@login_required
def decline_friend_request_view(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    if request.method == 'POST':
        friend_request.delete()
    return redirect('my_profile')

@login_required
def dismiss_notification_view(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if request.method == 'POST':
        notification.delete()
    return redirect('my_profile')

@login_required
def clear_all_notifications_view(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user).delete()
        FriendRequest.objects.filter(to_user=request.user).delete()
    return redirect('my_profile')


def about_us_view(request):
    """
    This view simply renders the static 'About Us' page.
    """
    return render(request, 'about.html')