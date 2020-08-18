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

def parseDateTime(a):

    now = a
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    if len(str(hour)) == 1:
        hour = f'0{hour}'

    if len(str(minute)) == 1:
        minute = f'0{minute}'

    if month == 1:
        month = 'Enero'
    elif month == 2:
        month = 'Febrero'
    elif month == 3:
        month = 'Marzo'
    elif month == 4:
        month = 'Abril'
    elif month == 5:
        month = 'Mayo'
    elif month == 6:
        month = 'Junio'
    elif month == 7:
        month = 'Julio'
    elif month == 8:
        month = 'Agosto'
    elif month == 9:
        month = 'Septiembre'
    elif month == 10:
        month = 'Octubre'
    elif month == 11:
        month = 'Noviembre'
    elif month == 12:
        month = 'Diciembre'
        
    return f'{day} de {month} del {year} - {hour}:{minute}'

def saldo(request):
    title = "Cuenta"
    if not request.user.is_authenticated:
        return redirect('/login')
    
    balance = Banking.objects.filter(user=request.user.id).values('balance', 'cvu')

    notifications = Notification.objects.filter(user=request.user.id)
    
    if not Banking.objects.filter(user=request.user.id):
        account = Cuenta.objects.get(id=request.user.id)
        balance_user_id = Banking(user=account, balance=0, cvu=None)
        balance_user_id.save()
    
    return render(request, "saldo.html", {'balance' : balance, 'title' : title, 'notifications' : notifications})

def balance(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    balance = Banking.objects.get(user=request.user.id)
    
    if request.method == 'POST':
        
        total_balance = request.POST.get('total_balance')

        try:
            if total_balance == "" or float(total_balance) == 0:
                messages.info(request, 'Ingresá un monto distinto a 0.')
                return HttpResponseRedirect('/cuenta')
                
            
            if 'add_balance' in request.POST:
                a = Cuenta.objects.get(id=request.user.id)
                formatted_balance = float(total_balance)
                b = Transactions(user=a, cash_moved=float(formatted_balance), type_of_move='Ingreso', date=parseDateTime(datetime.now()))
                balance.balance += float(formatted_balance)
                balance.save()
                b.save()
            
            if 'remove_balance' in request.POST:
                
                if float(total_balance) > balance.balance:
                    messages.info(request, 'El monto que estás queriendo retirar es mayor al que poseés.')
                    return HttpResponseRedirect('/cuenta')
                if float(total_balance) < 3:
                    messages.info(request, 'El monto mínimo para retirar es $ 3.')
                    return HttpResponseRedirect('/cuenta')
                a = Cuenta.objects.get(id=request.user.id)
                formatted_balance = "{:.2f}".format(float(total_balance))
                b = Transactions(user=a, cash_moved=float(formatted_balance), type_of_move='Retiro', date=parseDateTime(datetime.now()))
                balance.balance -= float(formatted_balance)
                balance.save()
                b.save()
        except ValueError:
            messages.info(request, 'Por favor, ingresá solo números.')
            return HttpResponseRedirect('/cuenta')
        
        return redirect('/cuenta')

def create_cvu(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    user_cvu = Banking.objects.get(user=request.user.id)

    if not user_cvu.cvu == None:
        error = 'Ya contás con un CVU.'
        return render(request, "error.html", {'error' : error})

    cvus = Banking.objects.all().values('cvu')
    cvu_list = []

    for cvu in cvu_list:
        cvu_list.append(cvu)

    if request.method == 'POST':
        generated_cvu = randrange(1000000000000000, 9999999999999999)
        if generated_cvu not in cvu_list:
            user_cvu.cvu = f'000000{generated_cvu}'
            user_cvu.save()
            return redirect('/cuenta')
        else:
            return HttpResponse('Error, prueba nuevamente más tarde.')


def send_cash(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    all_accounts = Banking.objects.all()
    balance = Banking.objects.get(user=request.user.id)

    if request.method == 'POST':

        cash_for_send = request.POST.get('cash_for_send')
        addressee_cvu = request.POST.get('addressee_cvu')

        try:
            if addressee_cvu == balance.cvu:
                error = 'No podés enviarte dinero a vos mismo.'
                return render(request, "error.html", {'error' : error})

            if cash_for_send == "" or addressee_cvu == "":
                error = 'Completá todos los campos.'
                return render(request, "error.html", {'error' : error})

            if float(cash_for_send) > balance.balance:
                error = 'Estás enviando más dinero del que poseés. Intentá reducir el monto y probá nuevamente.'
                return render(request, "error.html", {'error' : error})
            
            if not float(cash_for_send) >= 3 or float(cash_for_send) < 0:
                error = 'El monto mínimo para enviar es $ 3'
                return render(request, "error.html", {'error' : error})
            
            cvu_list = []

            for i in all_accounts:
                cvu_list.append(i.cvu)
            
            print(cvu_list)

            if addressee_cvu in cvu_list:

                for i in all_accounts:

                    b = Cuenta.objects.get(id=request.user.id)
                    addressee_user = Banking.objects.get(cvu=addressee_cvu)
                    formatted_balance = float(cash_for_send)
                    addressee_user.balance += float(formatted_balance)
                    balance.balance -= float(formatted_balance)
                    addressee_user.save()
                    balance.save()

                    c = Banking.objects.get(cvu=balance.cvu)
                    user_notif = Cuenta.objects.get(email=addressee_user.user)
                    notification = Notification(user=user_notif, text=f"<p style='color: green;'>{request.user.first_name} {request.user.last_name} te ha transferido $ {intcomma(float(formatted_balance))}</p>")
                    a = Transferencias(from_user=b, to_user=addressee_user.user, from_cvu=c, to_cvu=addressee_user, cash_moved=float(formatted_balance), date=parseDateTime(datetime.now()))
                    notification.save()
                    a.save()

                    return redirect('/cuenta')
            
            error = 'El CVU que ingresaste no existe. Verificá si lo estás ingresando correctamente.'
            return render(request, "error.html", {'error' : error})
        except ValueError:
            error = 'Por favor, ingresá solo números.'
            return render(request, "error.html", {'error' : error})
        
        return redirect('/cuenta')

def transactions(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    title = 'Transacciones'

    notifications = Notification.objects.filter(user=request.user.id)

    user_transactions = Transactions.objects.values('user__email', 'cash_moved', 'type_of_move', 'date').order_by('-id').filter(user=request.user.id)

    paginator = Paginator(user_transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions.html', {'page_obj' : page_obj, 'title' : title, 'notifications' : notifications})

def transferencias(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    title = 'Transferencias'

    notifications = Notification.objects.filter(user=request.user.id)

    user_transfers = Transferencias.objects.values('from_user__email', 'to_user__email', 'to_user__first_name', 'to_user__last_name', 'from_user__first_name', 'from_user__last_name', 'from_cvu__cvu', 'to_cvu__cvu', 'cash_moved', 'date').filter(Q(to_user__id=request.user.id) | Q(from_user__id=request.user.id)).order_by('-id')

    paginator = Paginator(user_transfers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transfers.html', {'page_obj' : page_obj, 'title' : title, 'notifications' : notifications})
