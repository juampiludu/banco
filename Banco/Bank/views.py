from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .form import RegistroForm

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

    form.fields['username'].help_text = None
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


