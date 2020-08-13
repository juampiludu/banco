from django.shortcuts import render, redirect, HttpResponse
from .models import Contacto
from datetime import datetime

def informe(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'POST':

        email = request.user.email
        nombre = request.user.first_name
        apellido = request.user.last_name
        motivo = request.POST.get('motivo')

        a = Contacto(email=email, nombre=nombre, apellido=apellido, motivo=motivo)
        a.save()

        return HttpResponse(status=204)

    return redirect('/saldo')
