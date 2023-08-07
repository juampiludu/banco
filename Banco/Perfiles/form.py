from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import Cuenta
from utils.is_user_under_age import is_user_under_age

PROVINCE_FIELDS = (
    ('first', '-- Seleccioná tu provincia --'),
    ('ba', 'Buenos Aires'),
    ('ct', 'Catamarca'),
    ('cc', 'Chaco'),
    ('ch', 'Chubut'),
    ('cb', 'Córdoba'),
    ('cn', 'Corrientes'),
    ('er', 'Entre Ríos'),
    ('fm', 'Formosa'),
    ('jy', 'Jujuy'),
    ('lp', 'La Pampa'),
    ('lr', 'La Rioja'),
    ('mz', 'Mendoza'),
    ('mn', 'Misiones'),
    ('nq', 'Neuquén'),
    ('rn', 'Río Negro'),
    ('sa', 'Salta'),
    ('sj', 'San Juan'),
    ('sl', 'San Luis'),
    ('sc', 'Santa Cruz'),
    ('sf', 'Santa Fe'),
    ('se', 'Santiago del Estero'),
    ('tf', 'Tierra del Fuego'),
    ('tm', 'Tucumán'),
)

class RegistroForm(UserCreationForm):

    first_name = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn second',
            'placeholder': '*Nombre',
        }
    ))

    last_name = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn third',
            'placeholder': '*Apellido',
        }
    ))

    born_date = forms.DateField(label="", required=True, widget=forms.TextInput(
        attrs={
            'type': 'date',
            'class': 'fadeIn fourth',
        }
    ))
    
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn fifth',
            'placeholder': '*Correo electrónico',
        }
    ))

    phone = forms.CharField(label="", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn sixth',
            'placeholder': 'Teléfono',
            'onkeypress': 'return valida(event);',
            'type': 'tel',
        }
    ))

    dni = forms.CharField(label="", max_length=8, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn seventh',
            'placeholder': '*DNI',
            'onkeypress': 'return valida(event);',
            'type': 'tel',
        }
    ))

    address = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn eighth',
            'placeholder': 'Domicilio',
        }
    ))

    password1 = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'fadeIn ninth',
            'placeholder': 'Contraseña',
        }
    ))

    password2 = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'fadeIn tenth',
            'placeholder': 'Repita contraseña',
        }
    ))

    province = forms.ChoiceField(choices=PROVINCE_FIELDS, label='', required=False, widget=forms.Select(
        attrs={
            'class' : 'fadeIn eighth',
        }
    ))

    city = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'fadeIn seventh',
            'placeholder': 'Ciudad',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        if Cuenta.objects.filter(email=email).exists():
            raise forms.ValidationError(f'El email "{email}" ya está en uso')
        return email

    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()
    
    def clean_born_date(self):
        born_date = self.cleaned_data['born_date']
        if is_user_under_age(born_date):
            raise forms.ValidationError('Tenés que ser mayor de 18 años para poder crear tu cuenta')
        return born_date
    
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if Cuenta.objects.filter(dni=dni).exists():
            raise forms.ValidationError(f'El DNI "{dni}" ya está registrado. Tal vez te hayas registrado previamente')
        return dni
    
    def clean_province(self):
        province = self.cleaned_data['province']
        if not province:
            raise forms.ValidationError("Seleccioná una provincia")
        return province

    class Meta:
        model = Cuenta
        fields = (
            'email',    
            'first_name',
            'last_name',
            'born_date',
            'phone',
            'dni',
            'province',
            'city',
            'address',
            'password1',
            'password2',
        )

class ActualizarForm(UserChangeForm):

    phone = forms.CharField(label="Teléfono", max_length=14, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'onkeypress': 'return valida(event);',
            'type': 'tel',
            'placeholder': 'Teléfono',
        }
    ))

    address = forms.CharField(label="Domicilio", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Domicilio',
        }
    ))

    province = forms.ChoiceField(choices=PROVINCE_FIELDS)

    city = forms.CharField(label="", max_length=140, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad',
        }
    ))

    def clean_province(self):
        province = self.cleaned_data['province']
        if not province:
            raise forms.ValidationError("Seleccioná una provincia")
        return province

    class Meta:
        model = Cuenta
        fields = (
            'phone',
            'address',
            'city',
            'province',
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
            'autocomplete': 'off',
        }
    ))

    new_password2 = forms.CharField(label='Confirme nueva contraseña:', widget=forms.TextInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            'autocomplete': 'off',
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
            'placeholder': 'Correo electrónico',
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
