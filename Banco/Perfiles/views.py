from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from .form import RegistroForm, ActualizarForm, CambiarContraForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.contrib import messages

def welcome(request):
    if request.user.is_authenticated:
        return render(request, "welcome.html")
    return redirect('/login')

def register(request):
    form = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            if user is not None:
                do_login(request, user)
                return redirect('/')

    form.fields['email'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    return render(request, "register.html", {'form': form})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            
            if user is not None:
                do_login(request, user)
                return redirect('/')

    return render(request, "login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('/')

def info(request):
    return render(request, "info.html")

def contactos(request):
    return render(request, "contactos.html")

def saldo(request):
    return render(request, "saldo.html")

def perfil(request):
    if request.method == "POST":
        form = ActualizarForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/perfil')
    else:
        form = ActualizarForm(instance=request.user)
        return render(request, "perfil.html", {'form': form})

def cambiar_contraseña(request):
    if request.method == "POST":
        form = CambiarContraForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/perfil')
        else:
            messages.error(request, 'Error')
            return HttpResponseRedirect("/perfil/actualizar-contraseña")
    else:
        form = CambiarContraForm(request.user)
        return render(request, 'perfil/change_pass.html', { 'form': form })