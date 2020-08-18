from django.contrib import admin
from django.urls import path, include
from Perfiles import views
from Perfiles import form
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),


    # register and confirmation of account

    path('register/', views.register),
    path('activar/<uidb64>/<token>', views.activate, name='activate'),

    # main urls

    path('', views.welcome),
    path('login/', views.login, name="login"),
    path('logout/', views.logout),
    path('about-us/', views.info),
    path('info-personal/', views.perfil),
    path('info-personal/actualizar-contraseña/', views.cambiar_contraseña),
    path('personas/', views.search_view, name="search_view"),

    # includes

    path('', include('banking.urls')),
    path('', include('user_contact.urls')),

    # reset password views

    path('reset/', auth_views.PasswordResetView.as_view(template_name="perfil/restablecer_contra_form.html", html_email_template_name="perfil/password_reset_email.html", subject_template_name="perfil/reset_password_email_subject.txt", title="Restablecer Contraseña"), name="password_reset"),
    path('reset/done',auth_views.PasswordResetDoneView.as_view(template_name="perfil/restablecer_contra_terminado.html", title="Correo enviado"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="perfil/restablecer_contra_confirm.html", title="Nueva Contraseña"), name='password_reset_confirm'),
    path('reset/completed', auth_views.PasswordResetCompleteView.as_view(template_name="perfil/restablecer_contra_completado.html", title="Finalizado"), name='password_reset_complete'),
]
