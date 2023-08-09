from django.urls import path
from . import views

urlpatterns = [
    
    path('seen/<id>', views.notif_seen, name="notif_seen"),

]
