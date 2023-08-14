from .models import Notification

def display_notifications(request):
    notifications = Notification.objects.filter(user=request.user.id).order_by('-id')
    return {'notifications': notifications}