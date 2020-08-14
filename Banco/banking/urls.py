from django.urls import path, include
from banking import views

urlpatterns = [
    path('cuenta/', views.saldo),
    path('cuenta/balance/', views.balance, name="balance"),
    path('cuenta/create_cvu/', views.create_cvu, name="create_cvu"),
    path('cuenta/send_cash/', views.send_cash, name="send_cash"),
    path('actividad/transacciones/', views.transactions, name='transactions'),
    path('actividad/transferencias/', views.transferencias, name='transferencias'),
]
