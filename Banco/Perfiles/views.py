from typing import Any, Dict, Optional
from django.db.models.query import QuerySet
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
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from utils.generar_cvu import generar_cvu
from django_email_verification import send_email, verify_view, verify_token
from django.db import IntegrityError, models
from utils.bank_constants import bank_constants
from django.views.generic import ListView
from django.contrib.auth.views import PasswordChangeView


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
    
    context = {
        'msg': bank_constants.ACTIVATED_ACCOUNT,
        'success': success
    }

    return render(request, 'registration/message.html', context)


class LoginView(DefaultLoginView, UserPassesTestMixin):
    form_class = LoginForm
    template_name = "login.html"

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_LOGIN
        return context


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

        send_email(user)

        messages.SUCCESS(bank_constants.EMAIL_SENT)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_REGISTER
        return context


class SearchUserView(ListView):
    model = Banking
    template_name = "search.html"
    context_object_name = "all_bankings"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            queryset = Banking.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
        else:
            queryset = Banking.objects.all()

        items_per_page = bank_constants.ITEMS_PER_PAGE
        paginator = Paginator(queryset, items_per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        return page_obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_SEARCH
        return context
    

class UserInfoView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    template_name = "perfil.html"
    context_object_name = "user"
    form_class = ActualizarForm

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('info_personal')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_PROFILE
        return context
    

class UpdatePasswordView(PasswordChangeView):
    template_name = "perfil/change_pass.html"
    form_class = CambiarContraForm
    success_url = reverse_lazy('info_personal')