from django.shortcuts import render, redirect
from .models import Banking
from Perfiles.models import Cuenta
from random import randrange

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
            balance.balance += float(total_balance)
            balance.save()
        
        if 'remove_balance' in request.POST:
            
            if float(total_balance) > balance.balance:
                error = 'El monto que estás queriendo retirar es mayor al que posees.'
                return render(request, "error.html", {'error' : error})
            if float(total_balance) < 3:
                error = 'El monto mínimo para retirar es $ 3.'
                return render(request, "error.html", {'error' : error})
            balance.balance -= float(total_balance)
            balance.save()
        
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
            error = 'Estás enviando más dinero del que posees. Intentá reducir el monto y probá nuevamente.'
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

                addressee_user = Banking.objects.get(cvu=addressee_cvu)
                addressee_user.balance += float(cash_for_send)
                balance.balance -= float(cash_for_send)
                addressee_user.save()
                balance.save()

                return redirect('/saldo')
        
        error = 'El CVU que ingresaste no existe. Verificá si lo estás ingresando correctamente.'
        return render(request, "error.html", {'error' : error})
        
        return redirect('/saldo')
