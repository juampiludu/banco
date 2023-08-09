from typing import Any, Dict, Optional, Type
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .form import RegistroForm, ActualizarForm, CambiarContraForm, LoginForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from apps.banking.models import Banking
from django.core import serializers
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from apps.notifications.models import Notification

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
from django.http import JsonResponse
from utils.georefar import georefar
from django.views import View
import pandas as pd
from django.utils import timezone
from django.contrib.staticfiles import finders


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

def get_new_localidades(request):
    provincia_id = request.GET.get('provincia_id')
    
    new_choices = georefar.get_localidades(provincia_id)

    return JsonResponse({'choices': new_choices})

@verify_view
def activate_account(request, token):
    success, user = verify_token(token)

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


class LoginView(UserPassesTestMixin, DefaultLoginView):
    form_class = LoginForm
    template_name = "login.html"
    login_url = reverse_lazy('landing')

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
    login_url = reverse_lazy('landing')

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.method == 'POST':
            selected_provincia = form.data['province']
            updated_localidad_choices = georefar.get_localidades(selected_provincia)
            form.fields['localidad'].choices = updated_localidad_choices
        
        return form
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_unusable_password()
        user.save()

        send_email(user)

        messages.success(self.request, bank_constants.EMAIL_SENT)

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
            queryset = Banking.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)).order_by('user__first_name')
        else:
            queryset = Banking.objects.all().order_by('user__first_name')

        items_per_page = bank_constants.ITEMS_PER_PAGE
        paginator = Paginator(queryset, items_per_page)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        return page_obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_SEARCH
        notifications = Notification.objects.filter(user=self.request.user.id).order_by('-id')
        context['notifications'] = notifications
        return context
    

class UserInfoView(LoginRequiredMixin, UpdateView):
    model = CuentaModel
    template_name = "perfil.html"
    context_object_name = "user"
    form_class = ActualizarForm
    success_url = reverse_lazy('info_personal')
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_PROFILE
        notifications = Notification.objects.filter(user=self.request.user.id).order_by('-id')
        context['notifications'] = notifications
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.method == 'POST':
            selected_provincia = form.data['province']
        else:
            selected_provincia = form.initial['province']

        updated_localidad_choices = georefar.get_localidades(selected_provincia)
        form.fields['localidad'].choices = updated_localidad_choices
        
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Datos actualizados correctamente')
        return super().form_valid(form)
    

class UpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_pass.html"
    form_class = CambiarContraForm
    success_url = reverse_lazy('info_personal')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Contraseña actualizada')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_CHANGE_PASS
        notifications = Notification.objects.filter(user=self.request.user.id).order_by('-id')
        context['notifications'] = notifications
        return context
    

class PrecioSurtidorView(View):
    def get(self, request):
        context = {
            'title': 'Precios surtidores'
        }
        return render(request, 'precios_en_surtidor.html', context)
    
    def post(self, request):
        province = request.POST.get('province')

        sanitized_province = province.replace('_', ' ')

        # NOTE: More info in http://datos.energia.gob.ar/dataset/precios-en-surtidor/archivo/80ac25de-a44a-4445-9215-090cf55cfda5
        # file: http://datos.energia.gob.ar/dataset/1c181390-5045-475e-94dc-410429be4b17/resource/80ac25de-a44a-4445-9215-090cf55cfda5/download/precios-en-surtidor-resolucin-3142016.csv
        csv_file_path = finders.find('other/precios-en-surtidor-resolucin-3142016.csv')

        data = pd.read_csv(csv_file_path)

        data['indice_tiempo'] = pd.to_datetime(data['indice_tiempo'])

        # NOTE: the file has to be updated every month by the owner to match current date (and downloaded every hour to keep it updated!)
        current_date = timezone.now().strftime('%Y-%m')
        filtered_data = data[data['indice_tiempo'].dt.strftime('%Y-%m') == current_date]

        specific_province = sanitized_province
        province_filtered_data = filtered_data[filtered_data['provincia'] == specific_province]

        grouped_data = province_filtered_data.groupby(['empresabandera', 'producto'])['precio'].mean().reset_index()

        data_list = grouped_data.to_dict(orient='records')

        context = {
            'province': province,
            'data': data_list,
            'title': 'Precios surtidores'
        }

        return render(request, 'precios_en_surtidor.html', context)