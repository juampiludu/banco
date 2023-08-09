from django.shortcuts import redirect
from .models import Notification

def notif_seen(request, id):
    notif = Notification.objects.get(id=id)
    notif.delete()
    return redirect('transferencias')

