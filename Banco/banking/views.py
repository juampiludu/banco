from django.shortcuts import render, redirect
from .models import Banking, Transactions, Transferencias
from Perfiles.models import Cuenta
from random import randrange
from datetime import datetime

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
    title = "Saldo"
    if not request.user.is_authenticated:
        return redirect('/login')
    
    balance = Banking.objects.filter(user=request.user.id).values('balance', 'cvu')
    
    if not Banking.objects.filter(user=request.user.id):
        account = Cuenta.objects.get(id=request.user.id)
        balance_user_id = Banking(user=account, balance=0, cvu=None)
        balance_user_id.save()
    
    return render(request, "saldo.html", {'balance' : balance, 'title' : title})

def balance(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    balance = Banking.objects.get(user=request.user.id)
    
    if request.method == 'POST':
        
        total_balance = request.POST.get('total_balance')
        
        if total_balance == "" or total_balance == '0':
            error = 'Ingresá un monto.'
            return render(request, "error.html", {'error' : error})
        
        if 'add_balance' in request.POST:
            a = Cuenta.objects.get(id=request.user.id)
            b = Transactions(user=a, cash_moved=f'+{total_balance}', type_of_move='Ingreso', date=parseDateTime(datetime.now()))
            balance.balance += float(total_balance)
            balance.save()
            b.save()
        
        if 'remove_balance' in request.POST:
            
            if float(total_balance) > balance.balance:
                error = 'El monto que estás queriendo retirar es mayor al que poseés.'
                return render(request, "error.html", {'error' : error})
            if float(total_balance) < 3:
                error = 'El monto mínimo para retirar es $ 3.'
                return render(request, "error.html", {'error' : error})
            a = Cuenta.objects.get(id=request.user.id)
            b = Transactions(user=a, cash_moved=f'-{total_balance}', type_of_move='Retiro', date=parseDateTime(datetime.now()))
            balance.balance -= float(total_balance)
            balance.save()
            b.save()
        
        return redirect('/saldo')

def create_cvu(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    user_cvu = Banking.objects.get(user=request.user.id)

    if request.method == 'POST':
        generated_cvu = randrange(1000000000000000, 1999999999999999)
        user_cvu.cvu = f'000000{generated_cvu}'
        user_cvu.save()
        return redirect('/saldo')


def send_cash(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    all_accounts = Banking.objects.all()
    balance = Banking.objects.get(user=request.user.id)

    if request.method == 'POST':

        cash_for_send = request.POST.get('cash_for_send')
        addressee_cvu = request.POST.get('addressee_cvu')

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
                addressee_user.balance += float(cash_for_send)
                balance.balance -= float(cash_for_send)
                addressee_user.save()
                balance.save()

                c = Banking.objects.get(cvu=balance.cvu)
                a = Transferencias(from_user=b, to_user=addressee_user.user, from_cvu=c, to_cvu=addressee_user, cash_sended=str(f'+{cash_for_send}'), cash_losed=str(f'-{cash_for_send}'), date=parseDateTime(datetime.now()))
                a.save()

                return redirect('/saldo')
        
        error = 'El CVU que ingresaste no existe. Verificá si lo estás ingresando correctamente.'
        return render(request, "error.html", {'error' : error})
        
        return redirect('/saldo')

def movimientos(request):
    title = "Movimientos"
    if not request.user.is_authenticated:
        return redirect('/login')
    user_transfers = Transferencias.objects.values('from_user__email', 'to_user__email', 'to_user__first_name', 'to_user__last_name', 'from_user__first_name', 'from_user__last_name', 'from_cvu__cvu', 'to_cvu__cvu', 'cash_losed', 'cash_sended', 'date').order_by('-id')
    user_transactions = Transactions.objects.values('user__email', 'cash_moved', 'type_of_move', 'date').order_by('-id')
    return render(request, "movimientos.html", {'title' : title, 'user_transfers' : user_transfers, 'user_transactions' : user_transactions})
