from apps.banking.models import Banking
from .generar_cvu import generar_cvu
from django.db import IntegrityError

def create_banking(user):
    banking = Banking()
    banking.user = user

    while True:
        try:
            banking.cvu = generar_cvu()
            break
        except IntegrityError:
            continue

    banking.save()