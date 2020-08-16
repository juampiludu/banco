from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import RegistroForm, ActualizarForm, CambiarContraForm, LoginForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from banking.models import Banking
from django.core import serializers
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Cuenta
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


CuentaModel = get_user_model()


def welcome(request):
    title = "Inicio"
    all_users = Cuenta.objects.all()
    return render(request, "welcome.html", {'title' : title, 'all_users' : all_users})

def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    title = 'Registrarse'

    if request.method == "POST":

        form = RegistroForm(request.POST)

        a = request.POST.get('born_date')
        b = datetime.strptime(a, '%Y-%m-%d')
        age = datetime.now() - b

        if age.days < 6575:

            error = "Tenés que ser mayor de 18 años para registrarte."
            return render(request, 'error.html', {'error': error})

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activá tu cuenta.'
            email_html = render_to_string('registration/confirm_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            message = strip_tags(email_html)
            to_email = form.cleaned_data.get('email')

            email = EmailMultiAlternatives(mail_subject, message, 'lu.dev.spprt@gmail.com', [to_email])
            email.attach_alternative(email_html, "text/html")
            email.send()

            title = "Confirmá tu correo"
            msg = 'Por favor, confirmá tu correo electrónico para completar el registro.'
            return render(request, 'registration/message.html', {'msg' : msg, 'title' : title})

    form = RegistroForm()

    return render(request, "registration/register.html", {'form': form, 'title' : title})

def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CuentaModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        title = 'Correo Confirmado'
        msg = 'Gracias por confirmar tu correo. Ahora podés <a href="/login">acceder</a> a la página.'
        return render(request, 'registration/message.html', {'msg' : msg, 'title' : title})
    else:
        title = 'Link inválido'
        msg = 'El link de activación es inválido.'
        return render(request, 'registration/message.html', {'msg' : msg, 'title' : title})


def login(request):
    title = 'Iniciar Sesión'
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
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
    title = "Sobre Nosotros"
    return render(request, "info.html", {'title' : title})

def perfil(request):
    title = "Información Personal"
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        form = ActualizarForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/info-personal')
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
            return redirect('/info-personal')
        else:
            messages.error(request, 'Ha ocurrido un error. Ingrese los datos de manera correcta e intente nuevamente.')
            return HttpResponseRedirect("/info-personal/actualizar-contraseña")
    
    return render(request, 'perfil/change_pass.html', { 'form': form })

def search_view(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    title = "Búsqueda"

    search = request.GET.get('search')

    if search == '':
        all_users_query = Banking.objects.values('user__email', 'cvu', 'user__first_name', 'user__last_name').exclude(cvu=None).order_by('user__last_name')
    else:
        all_users_query = Banking.objects.values('user__email', 'cvu', 'user__first_name', 'user__last_name').filter(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(user__email__icontains=search)).exclude(cvu=None).order_by('user__last_name')

    paginator = Paginator(all_users_query, 20)
    page_number = request.GET.get('page')
    all_users = paginator.get_page(page_number)

    return render(request, 'search.html', {'search' : search, 'all_users' : all_users, 'title' : title})