from django.shortcuts import render, HttpResponse, redirect
from .models import Notification

def notif_viewed(request, id):

    notif = Notification.objects.filter(id=id)
    
    user_notif = None

    for i in notif:
        user_notif = i.user

    if not str(request.user.email) == str(user_notif) or not request.user.is_authenticated:
        return HttpResponse("Error")

    notif.delete()

    return redirect('transferencias')

