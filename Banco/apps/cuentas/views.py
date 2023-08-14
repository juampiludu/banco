from typing import Any, Optional
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from .form import RegistroForm, ActualizarForm, CambiarContraForm, LoginForm, CompletarRegistroForm
from django.contrib import messages
from apps.banking.models import Banking
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Cuenta
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from utils.generar_cvu import generar_cvu
from django_email_verification import send_email, verify_view, verify_token
from django.db import IntegrityError, models
from utils.bank_constants import bank_constants
from django.views.generic import ListView
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest, HttpResponse, JsonResponse
from utils.georefar import georefar
from django.views import View
import pandas as pd
from django.utils import timezone
from django.contrib.staticfiles import finders
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from utils.create_banking import create_banking
from allauth.socialaccount.models import SocialAccount


CuentaModel = get_user_model()


def welcome(request):
    title = "Inicio"
    all_users = Cuenta.objects.all()
    return render(request, "welcome.html", {'title' : title, 'all_users' : all_users})

def logout(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    do_logout(request)
    return redirect('/')

def info(request):
    title = "Sobre Nosotros"
    return render(request, "info.html", {'title' : title})

def get_new_localidades(request):
    provincia_id = request.GET.get('provincia_id')
    
    new_choices = georefar.get_localidades(provincia_id)

    return JsonResponse({'choices': new_choices})

@verify_view
def activate_account(request, token):
    success, user = verify_token(token)

    if success:
        create_banking(user)
    
    context = {
        'msg': bank_constants.ACTIVATED_ACCOUNT,
        'success': success
    }

    return render(request, 'registration/message.html', context)

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = True
    user.save()

def is_social(self):
    return SocialAccount.objects.filter(user=self.request.user).exists()


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
        return context
    

class UserInfoView(LoginRequiredMixin, UpdateView):
    model = CuentaModel
    template_name = "perfil.html"
    context_object_name = "user"
    form_class = ActualizarForm
    success_url = reverse_lazy('info_personal')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_PROFILE
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

    def get(self, request, *args, **kwargs):
        if is_social(self):
            return redirect('info_personal')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Contraseña actualizada')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_CHANGE_PASS
        return context
    

class CompletarRegistroView(LoginRequiredMixin, UpdateView):
    model = CuentaModel
    template_name = "registration/completar_registro.html"
    form_class = CompletarRegistroForm
    context_object_name = "user"
    success_url = reverse_lazy('landing')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = bank_constants.TITLE_COMP_REGISTRO
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
        messages.success(self.request, 'Tu cuenta ha sido creada con éxito')
        self.request.user.profile_completed = True
        self.request.user.save()
        create_banking(self.request.user)
        return super().form_valid(form)


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