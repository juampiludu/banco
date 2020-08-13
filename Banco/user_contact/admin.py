from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = ('email', 'motivo', 'fecha')
