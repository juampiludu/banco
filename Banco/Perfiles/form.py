from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import Cuenta

class RegistroForm(UserCreationForm):

    first_name = forms.CharField(label="Nombre", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    last_name = forms.CharField(label="Apellido", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    born_date = forms.DateField(label="Fecha de nacimiento", required=True, initial='2019-01-01', widget=forms.TextInput(
        attrs={
            'type': 'date',
        }
    ))
    
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    phone = forms.CharField(label="Teléfono", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    dni = forms.CharField(label="DNI", max_length=8, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    direction = forms.CharField(label="Dirección", max_length=140, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    password1 = forms.CharField(label='Contraseña', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
        }
    ))

    password2 = forms.CharField(label='Repita contraseña', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
        }
    ))

    class Meta:
        model = Cuenta
        fields = (
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

class ActualizarForm(UserChangeForm):

    first_name = forms.CharField(label="Nombre", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    last_name = forms.CharField(label="Apellido", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    born_date = forms.DateField(label="Fecha de nacimiento", required=True, initial='2019-01-01', widget=forms.TextInput(
        attrs={
            'type': 'date',
        }
    ))
    
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        }
    ))

    phone = forms.CharField(label="Teléfono", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    dni = forms.CharField(label="DNI", max_length=8, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        }
    ))

    direction = forms.CharField(label="Dirección", max_length=140, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    password = forms.CharField(label='Contraseña', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'readonly': 'readonly',
        }
    ))

    class Meta:
        model = Cuenta
        fields = (
            'email',    
            'first_name',
            'last_name',
            'born_date',
            'phone',
            'dni',
            'direction',
            'password',
        )

class CambiarContraForm(PasswordChangeForm):

    old_password = forms.CharField(label='Actual contraseña:', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
        }
    ))

    new_password1 = forms.CharField(label='Nueva contraseña:', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
        }
    ))

    new_password2 = forms.CharField(label='Confirme nueva contraseña:', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
        }
    ))

    class Meta:
        model = Cuenta
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )