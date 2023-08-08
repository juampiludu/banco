from django.shortcuts import redirect, HttpResponse
from .models import Contacto

def informe(request):
    if request.method == 'POST':
        user = request.user
        motivo = request.POST.get('motivo')

        Contacto.objects.create(user=user, motivo=motivo)

        return HttpResponse(status=204)

    return redirect('cuenta')
