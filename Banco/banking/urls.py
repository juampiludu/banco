from django.urls import path, include
from banking.views import *

urlpatterns = [
    path('cuenta/', CuentaView.as_view(), name="cuenta"),
    path('actividad/transacciones/', TransactionsView.as_view(), name='transactions'),
    path('actividad/transferencias/', TransfersView.as_view(), name='transferencias'),
]
