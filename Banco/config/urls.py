from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls
from apps.cuentas import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # login, register and confirmation of account

    path('login/', main_views.LoginView.as_view(), name="login"),
    path('logout/', main_views.logout, name='logout'),
    path('register/', main_views.RegisterView.as_view(), name="register"),
    path('activar/<token>', main_views.activate_account, name='activate_account'),

    # main urls

    path('', main_views.welcome, name='landing'),
    path('sobre-nosotros/', main_views.info, name='sobre_nosotros'),
    path('precios-en-surtidor/', main_views.PrecioSurtidorView.as_view(), name="precios_en_surtidor"),
    path('get-new-localidades/', main_views.get_new_localidades, name='get_new_localidades'),

    # includes

    path('banking/', include('apps.banking.urls')),
    path('contact/', include('apps.user_contact.urls')),
    path('notificaciones/', include('apps.notifications.urls')),
    path('cuentas/', include('apps.cuentas.urls')),
    # path('accounts/', include('allauth.urls')),

    # reset password views

    path('reset/', auth_views.PasswordResetView.as_view(template_name="reset_pass/restablecer_contra_form.html", html_email_template_name="reset_pass/password_reset_email.html", subject_template_name="reset_pass/reset_password_email_subject.txt", title="Restablecer Contraseña"), name="password_reset"),
    path('reset/done',auth_views.PasswordResetDoneView.as_view(template_name="reset_pass/restablecer_contra_terminado.html", title="Correo enviado"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="reset_pass/restablecer_contra_confirm.html", title="Nueva Contraseña"), name='password_reset_confirm'),
    path('reset/completed', auth_views.PasswordResetCompleteView.as_view(template_name="reset_pass/restablecer_contra_completado.html", title="Finalizado"), name='password_reset_complete'),
]
