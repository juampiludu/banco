from django.contrib import admin
from .models import Banking

@admin.register(Banking)
class BankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'cvu')