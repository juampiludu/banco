from django.db import models
from Perfiles.models import Cuenta

class Banking(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    cvu = models.CharField(max_length=22, default=None, null=True, unique=True)
