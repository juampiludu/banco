from django.shortcuts import render, redirect, HttpResponse
from .models import Banking, Transactions, Transferencias
from apps.cuentas.models import Cuenta
from random import randrange
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from apps.notifications.models import Notification
from django.contrib.humanize.templatetags.humanize import intcomma
from django.views import View
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from utils.exceptions import SameAccount
from django.utils import timezone
from utils.bank_constants import bank_constants
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


def parse_string_to_decimal(currency_string):
    substring = currency_string.replace('$', '').replace('.', '').split(',')
    decimal_number = Decimal(substring[0] + '.' + substring[1])
    return decimal_number


def create_notificacion(request, receiver_user, amount):
    notif = Notification()
    notif.user = receiver_user
    notif.text = f"{request.user.get_full_name()} te ha enviado $ {amount}"
    notif.save()

def cuenta_ingresar(request, banking):
    with transaction.atomic():
        amount = parse_string_to_decimal(request.POST["total_balance"])
        if amount <= 0.01:
            messages.error(request, bank_constants.MIN_CANT_ING, extra_tags="#ing")
            return redirect("banking")
        banking.balance += amount
        Transactions.objects.create(user=request.user, amount=amount, is_ingreso=True, timestamp=timezone.now())

def cuenta_retirar(request, banking):
    with transaction.atomic():
        amount = parse_string_to_decimal(request.POST["total_balance"])
        if amount > banking.balance:
            messages.error(request, bank_constants.SALD_INS, extra_tags="#ing")
            return redirect("banking")
        elif amount <= 0.01:
            messages.error(request, bank_constants.MIN_CANT_RET, extra_tags="#ing")
            return redirect("banking")
        banking.balance -= amount
        Transactions.objects.create(user=request.user, amount=amount, is_ingreso=False, timestamp=timezone.now())

def transferir(request, banking):
    with transaction.atomic():
        amount = parse_string_to_decimal(request.POST["transferir_amount"])
        receiver_cvu = request.POST["transferir_cvu"]
        if amount <= 0.01:
            messages.error(request, bank_constants.MIN_CANT_TRANS, extra_tags="#trans-cant")
            return redirect("banking")
        elif amount > banking.balance:
            messages.error(request, bank_constants.SALD_INS, extra_tags="#trans-cant")
            return redirect("banking")
        try:
            receiver = Banking.objects.get(cvu=receiver_cvu)
            if receiver == banking:
                raise SameAccount()
            receiver.balance += amount
            banking.balance -= amount
            receiver.save()
            Transferencias.objects.create(sender=request.user, receiver=receiver.user, amount=amount, timestamp=timezone.now())
            create_notificacion(request, receiver.user, amount)
            messages.success(request, bank_constants.TRANS_SUCCESS, extra_tags="trans-success")
        except ObjectDoesNotExist:
            messages.error(request, bank_constants.CVU_INC, extra_tags="#trans-cvu")
        except SameAccount:
            messages.error(request, bank_constants.CVU_SAME, extra_tags="#trans-cvu")

class CuentaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        banking = Banking.objects.get(user=request.user)
        context = {'banking': banking, 'title': "Banking"}
        
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

        return redirect("banking")


class TransactionsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        transactions = Transactions.objects.all().filter(user=request.user).order_by('-timestamp')

        items_per_page = bank_constants.ITEMS_PER_PAGE
        paginator = Paginator(transactions, items_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'title': "Transacciones"}

        return render(request, "transactions.html", context)
    

class TransfersView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        transfers = Transferencias.objects.all().filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
        notifications = Notification.objects.filter(user=self.request.user.id)
        notifications.delete()

        items_per_page = bank_constants.ITEMS_PER_PAGE
        paginator = Paginator(transfers, items_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'title': "Transferencias"}

        return render(request, "transfers.html", context)