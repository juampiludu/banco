from django.contrib import admin
from .models import Banking, Transferencias, Transactions

@admin.register(Banking)
class BankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'cvu')

@admin.register(Transferencias)
class TransferenciasAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'cash_moved')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'cash_moved', 'type_of_move')