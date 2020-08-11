from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .form import RegistroForm, ActualizarForm, CambiarContraForm, LoginForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from banking.models import Banking
from django.core import serializers
from datetime import datetime

def welcome(request):
    title = "Inicio"
    return render(request, "welcome.html", {'title' : title})

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    title = 'Registrarse'
    form = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(data=request.POST)

        a = request.POST.get('born_date')
        b = datetime.strptime(a, '%Y-%m-%d')
        age = datetime.now() - b
        print(age)

        if age.days < 6575:
            error = "Tenés que ser mayor de 18 años para registrarte."
            return render(request, 'error.html', {'error', error})

        if form.is_valid():

            user = form.save()

            if user is not None:
                do_login(request, user)
                return redirect('/')

    #form.fields['email'].help_text = None
    #form.fields['password1'].help_text = None
    #form.fields['password2'].help_text = None

    return render(request, "register.html", {'form': form, 'title' : title})

def login(request):
    title = 'Iniciar Sesión'
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            
            if user is not None:
                do_login(request, user)
                return redirect('/')

    return render(request, "login.html", {'form': form, 'title' : title})

def logout(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    do_logout(request)
    return redirect('/')

def info(request):
    title = "Información"
    return render(request, "info.html", {'title' : title})

def perfil(request):
    title = "Perfil"
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        form = ActualizarForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/perfil')
    else:
        form = ActualizarForm(instance=request.user)
        return render(request, "perfil.html", {'form': form, 'title' : title})

def cambiar_contraseña(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    form = CambiarContraForm(request.user, request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/perfil')
        else:
            messages.error(request, 'Ha ocurrido un error. Ingrese los datos de manera correcta e intente nuevamente.')
            return HttpResponseRedirect("/perfil/actualizar-contraseña")
    
    return render(request, 'perfil/change_pass.html', { 'form': form })

def search_view(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    title = "Búsqueda"

    search = request.GET.get('search')

    all_users = Banking.objects.values('user__email', 'cvu', 'user__first_name', 'user__last_name').order_by('user__last_name')

    return render(request, 'search.html', {'search' : search, 'all_users' : all_users, 'title' : title})