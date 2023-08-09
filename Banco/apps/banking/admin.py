from django.contrib import admin
from .models import Banking, Transferencias, Transactions

@admin.register(Banking)
class BankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'cvu')

@admin.register(Transferencias)
class TransferenciasAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_ingreso')