from django.urls import path
from . import views

urlpatterns = [
    
    path('notification/<id>', views.notif_viewed, name="notif_viewed"),

]
