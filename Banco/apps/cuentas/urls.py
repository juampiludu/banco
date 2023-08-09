from django.urls import path
from apps.cuentas.views import *

urlpatterns = [
    path('info-personal/', UserInfoView.as_view(), name='info_personal'),
    path('info-personal/cambiar-contraseña/', UpdatePasswordView.as_view(), name="cambiar_contraseña"),
    path('personas/', SearchUserView.as_view(), name="search_view"),
]