from django.urls import path, include
from banking import views

urlpatterns = [
    path('', views.saldo),
    path('balance/', views.balance, name="balance"),
    path('create_cvu/', views.create_cvu, name="create_cvu"),
    path('send_cash/', views.send_cash, name="send_cash"),
]
