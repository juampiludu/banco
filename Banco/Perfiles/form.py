from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cuenta

class RegistroForm(UserCreationForm):

    first_name = forms.CharField(label="Nombre", max_length=140, required=True)
    last_name = forms.CharField(label="Apellido", max_length=140, required=True)
    born_date = forms.DateField(label="Fecha de nacimiento", required=True, widget=forms.SelectDateWidget)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Teléfono", max_length=14, required=True)
    dni = forms.CharField(label="DNI", max_length=8, required=True)
    direction = forms.CharField(label="Dirección", max_length=140, required=False)

    class Meta:
        model = Cuenta
        fields = (
            'username',
            'email',    
            'first_name',
            'last_name',
            'born_date',
            'phone',
            'dni',
            'direction',
            'password1',
            'password2',
        )

        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Repita contraseña',
        }