from django.contrib import admin
from django.urls import path, include
from Perfiles import views
from Perfiles import form
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),


    # login, register and confirmation of account

    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('activar/<token>', views.activate_account, name='activate_account'),

    # main urls

    path('', views.welcome, name='landing'),
    path('sobre-nosotros/', views.info, name='sobre_nosotros'),
    path('info-personal/', views.UserInfoView.as_view(), name='info_personal'),
    path('info-personal/cambiar-contraseña/', views.UpdatePasswordView.as_view(), name="cambiar_contraseña"),
    path('personas/', views.SearchUserView.as_view(), name="search_view"),
    path('get-new-localidades/', views.get_new_localidades, name='get_new_localidades'),

    # includes

    path('', include('banking.urls')),
    path('', include('user_contact.urls')),
    path('', include('notifications.urls')),
    # path('accounts/', include('allauth.urls')),

    # reset password views

    path('reset/', auth_views.PasswordResetView.as_view(template_name="perfil/restablecer_contra_form.html", html_email_template_name="perfil/password_reset_email.html", subject_template_name="perfil/reset_password_email_subject.txt", title="Restablecer Contraseña"), name="password_reset"),
    path('reset/done',auth_views.PasswordResetDoneView.as_view(template_name="perfil/restablecer_contra_terminado.html", title="Correo enviado"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="perfil/restablecer_contra_confirm.html", title="Nueva Contraseña"), name='password_reset_confirm'),
    path('reset/completed', auth_views.PasswordResetCompleteView.as_view(template_name="perfil/restablecer_contra_completado.html", title="Finalizado"), name='password_reset_complete'),
]
