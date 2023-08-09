from django.db import models
from apps.cuentas.models import Cuenta

class Contacto(models.Model):

    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    motivo = models.TextField()
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return f"Mensaje de {self.user.email}"
    
