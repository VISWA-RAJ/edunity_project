# core/context_processors.py
from .models import FriendRequest, Notification

def notification_processor(request):
    """
    This function provides the total UNREAD notification count to all templates.
    """
    if request.user.is_authenticated:
        # Count pending friend requests
        friend_request_count = FriendRequest.objects.filter(to_user=request.user).count()
        
        # Count other unread notifications
        unread_notification_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        
        # This is the total count that will be displayed in the navbar
        total_notifications = friend_request_count + unread_notification_count
        
        return {'total_notifications': total_notifications}
    return {}