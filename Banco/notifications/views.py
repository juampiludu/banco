from django.shortcuts import redirect
from .models import Notification

def notif_viewed(request, id):
    notif = Notification.objects.get(id=id)
    notif.delete()
    return redirect('transferencias')

