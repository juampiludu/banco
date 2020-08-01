from django.urls import path, include
from banking import views

urlpatterns = [
    path('saldo/', views.saldo),
    path('saldo/balance/', views.balance, name="balance"),
    path('saldo/create_cvu/', views.create_cvu, name="create_cvu"),
    path('saldo/send_cash/', views.send_cash, name="send_cash"),
    path('movimientos/', views.movimientos),
]
