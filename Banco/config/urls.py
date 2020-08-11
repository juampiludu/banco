"""Banco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Perfiles import views
from Perfiles import form
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome),
    path('register/', views.register),
    path('login/', views.login, name="login"),
    path('logout/', views.logout),
    path('info/', views.info),
    path('perfil/', views.perfil),
    path('perfil/actualizar-contraseña/', views.cambiar_contraseña),
    path('', include('banking.urls')),
    path('personas/', views.search_view, name="search_view"),

    path('admin/', admin.site.urls),

    path('reset/', auth_views.PasswordResetView.as_view(template_name="perfil/restablecer_contra_form.html"), name="password_reset"),
    path('reset/done',auth_views.PasswordResetDoneView.as_view(template_name="perfil/restablecer_contra_terminado.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="perfil/restablecer_contra_confirm.html"), name='password_reset_confirm'),
    path('reset/completed', auth_views.PasswordResetCompleteView.as_view(template_name="perfil/restablecer_contra_completado.html"), name='password_reset_complete'),
]
