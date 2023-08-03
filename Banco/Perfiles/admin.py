from django.contrib import admin
from .models import *

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_superuser')
    exclude = ('password',)