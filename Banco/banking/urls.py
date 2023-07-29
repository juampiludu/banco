from django.urls import path, include
from banking.views import *

urlpatterns = [
    path('cuenta/', CuentaView.as_view(), name="cuenta"),
    # path('actividad/transacciones/', views.transactions, name='transactions'),
    # path('actividad/transferencias/', views.transferencias, name='transferencias'),
]
