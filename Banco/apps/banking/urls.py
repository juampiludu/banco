from django.urls import path, include
from apps.banking.views import *

urlpatterns = [
    path('', CuentaView.as_view(), name="banking"),
    path('actividad/transacciones/', TransactionsView.as_view(), name='transacciones'),
    path('actividad/transferencias/', TransfersView.as_view(), name='transferencias'),
]
