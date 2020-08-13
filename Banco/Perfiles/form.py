from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import Cuenta

class RegistroForm(UserCreationForm):

    first_name = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn second',
            'placeholder': 'Nombre*',
        }
    ))

    last_name = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn third',
            'placeholder': 'Apellido*',
        }
    ))

    born_date = forms.DateField(label="", required=True, initial='2019-01-01', widget=forms.TextInput(
        attrs={
            'type': 'date',
            'class': 'fadeIn fourth',
        }
    ))
    
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn fifth',
            'placeholder': 'Correo Electrónico*',
        }
    ))

    phone = forms.CharField(label="", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn sixth',
            'placeholder': 'Teléfono',
        }
    ))

    dni = forms.CharField(label="", max_length=8, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn seventh',
            'placeholder': 'DNI*',
        }
    ))

    direction = forms.CharField(label="", max_length=140, required=False, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn eighth',
            'placeholder': 'Dirección',
        }
    ))

    password1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'fadeIn ninth',
            'placeholder': 'Contraseña',
        }
    ))

    password2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'fadeIn tenth',
            'placeholder': 'Repita Contraseña',
        }
    ))

    def clean_firstname(self):
        return self.cleaned_data['first_name'].capitalize()

    def clean_lastname(self):
        return self.cleaned_data['last_name'].capitalize()

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

    phone = forms.CharField(label="Teléfono", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    direction = forms.CharField(label="Dirección", max_length=140, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = Cuenta
        fields = (
            'phone',
            'direction',
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

class LoginForm(AuthenticationForm):

    username = forms.EmailField(label=False, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn second',
            'placeholder': 'Correo Electrónico',
            'name': 'username',
        }
    ))

    password = forms.CharField(label=False, widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'fadeIn third',
            'placeholder': 'Contraseña',
            'name': 'password',
        }
    ))
