from django.db import models
from Perfiles.models import Cuenta

class Contacto(models.Model):

    email = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    motivo = models.TextField()
    fecha = models.DateField(auto_now=True)

    def __str__(self):
        return self.email + ": " + self.motivo
    
