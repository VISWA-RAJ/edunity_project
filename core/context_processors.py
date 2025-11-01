# core/context_processors.py
from .models import FriendRequest, Notification

def notification_processor(request):
    """
    This function provides notification data to all templates.
    """
    if request.user.is_authenticated:
        # Get the actual objects for the dropdown
        # We don't slice friend requests, as they are all important
        pending_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        
        # Get the 5 most recent *unread* notifications
        recent_notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-timestamp')[:5]
        
        # Get the total counts for the badge
        friend_request_count = pending_friend_requests.count()
        # Get the count of ALL unread notifications, not just the recent 5
        total_unread_notification_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        
        # This is the total count that will be displayed in the navbar badge
        total_notifications = friend_request_count + total_unread_notification_count
        
        return {
            'total_notifications': total_notifications,
            'pending_friend_requests': pending_friend_requests,
            'recent_notifications': recent_notifications,
        }
    return {}