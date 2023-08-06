from django.shortcuts import render, redirect, HttpResponse
from .models import Banking, Transactions, Transferencias
from Perfiles.models import Cuenta
from random import randrange
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from notifications.models import Notification
from django.contrib.humanize.templatetags.humanize import intcomma
from django.views import View
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from utils.exceptions import SameAccount
from django.utils import timezone
from utils.bank_constants import bank_constants


def cuenta_ingresar(request, banking):
    with transaction.atomic():
        amount = Decimal(request.POST["total_balance"])
        if amount <= 0.01:
            messages.error(request, "La cantidad mínima para ingresar es de $0,01", extra_tags="cuenta")
            return redirect("cuenta")
        banking.balance += amount
        Transactions.objects.create(user=request.user, amount=amount, is_ingreso=True, timestamp=timezone.now())

def cuenta_retirar(request, banking):
    with transaction.atomic():
        amount = Decimal(request.POST["total_balance"])
        if amount > banking.balance:
            messages.error(request, "Saldo insuficiente", extra_tags="cuenta")
            return redirect("cuenta")
        banking.balance -= amount
        Transactions.objects.create(user=request.user, amount=amount, is_ingreso=False, timestamp=timezone.now())

def transferir(request, banking):
    with transaction.atomic():
        amount = Decimal(request.POST["transferir_amount"])
        receiver_cvu = request.POST["transferir_cvu"]
        try:
            receiver = Banking.objects.get(cvu=receiver_cvu)
            if receiver == banking:
                raise SameAccount()
            receiver.balance += amount
            banking.balance -= amount
            receiver.save()
            Transferencias.objects.create(sender=request.user, receiver=receiver.user, amount=amount, timestamp=timezone.now())
        except ObjectDoesNotExist:
            messages.error(request, "CVU incorrecto", extra_tags="cvu")
        except SameAccount:
            messages.error(request, "No podés transferirte vos mismo", extra_tags="cvu")
        finally:
            if amount <= 0.01:
                messages.error(request, "La cantidad mínima para transferir es de $0,01", extra_tags="min")
            elif amount > banking.balance:
                messages.error(request, "Saldo insuficiente", extra_tags="min")
            return redirect("cuenta")
        

class CuentaView(View):
    def get(self, request):
        banking = Banking.objects.get(user=request.user)
        context = {'banking': banking, 'title': "Cuenta"}
        
        return render(request, "saldo.html", context)
    
    def post(self, request):
        banking = Banking.objects.get(user=request.user)
        
        if "cuenta_ingresar" in request.POST:
            cuenta_ingresar(request, banking)
        elif "cuenta_retirar" in request.POST:
            cuenta_retirar(request, banking)
        elif "transferir" in request.POST:
            transferir(request, banking)

        banking.save()

        return redirect("cuenta")


class TransactionsView(View):
    def get(self, request):
        transactions = Transactions.objects.all().filter(user=request.user).order_by('-timestamp')

        items_per_page = 1
        paginator = Paginator(transactions, items_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'title': "Transacciones"}

        return render(request, "transactions.html", context)
    

class TransfersView(View):
    def get(self, request):
        transfers = Transferencias.objects.all().filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')

        items_per_page = bank_constants.ITEMS_PER_PAGE
        paginator = Paginator(transfers, items_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'title': "Transferencias"}

        return render(request, "transfers.html", context)