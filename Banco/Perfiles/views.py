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
from notifications.models import Notification

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Cuenta
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from utils.generar_cvu import generar_cvu
from django_email_verification import send_email, verify_view, verify_token
from django.db import IntegrityError


CuentaModel = get_user_model()


def welcome(request):
    title = "Inicio"
    all_users = Cuenta.objects.all()
    notifications = Notification.objects.filter(user=request.user.id).order_by('-id')
    return render(request, "welcome.html", {'title' : title, 'all_users' : all_users, 'notifications' : notifications})

def logout(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    do_logout(request)
    return redirect('/')

def info(request):
    title = "Sobre Nosotros"
    notifications = Notification.objects.filter(user=request.user.id).order_by('-id')
    return render(request, "info.html", {'title' : title, 'notifications' : notifications})

@verify_view
def activate_account(request, token):
    success, user = verify_token(token)

    if request.user != user or request.user.is_authenticated:
        return redirect('landing')

    try:
        if success:
            banking = Banking()
            banking.user = user
            banking.cvu = generar_cvu()
            banking.save()
    except IntegrityError:
        pass

    msg = 'Cuenta activada con éxito!'
    
    context = {
        'msg': msg,
        'success': success
    }

    return render(request, 'registration/message.html', context)


class LoginView(DefaultLoginView, UserPassesTestMixin):
    form_class = LoginForm
    template_name = "login.html"

    def test_func(self):
        return not self.request.user.is_authenticated


class RegisterView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    model = CuentaModel
    form_class = RegistroForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_unusable_password()
        user.save()

        # current_site = get_current_site(self.request)
        # domain = current_site.domain
        # protocol = 'https' if self.request.is_secure() else 'http'

        # activation_token = default_token_generator.make_token(user)
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # activation_link = reverse('activate_account', args=[uidb64, activation_token])
        # activation_url = f"{protocol}://{domain}{activation_link}"

        # mail_subject = 'Activá tu cuenta.'
        # email_html = render_to_string('registration/confirm_account.html', {
        #     'user': user,
        #     'activation_url': activation_url
        # })
        # message = strip_tags(email_html)
        # to_email = form.cleaned_data.get('email')

        # email = EmailMultiAlternatives(mail_subject, message, 'lu.dev.spprt@gmail.com', [to_email])
        # email.attach_alternative(email_html, "text/html")
        # email.send()

        send_email(user)

        return super().form_valid(form)