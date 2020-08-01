from django.db import models
from Perfiles.models import Cuenta

class Banking(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    cvu = models.CharField(max_length=22, default=None, null=True, unique=True)

class Transferencias(models.Model):
    from_user = models.ForeignKey(Cuenta, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(Cuenta, related_name="to_user", on_delete=models.CASCADE)
    from_cvu = models.ForeignKey(Banking, related_name="from_cvu", on_delete=models.CASCADE)
    to_cvu = models.ForeignKey(Banking, related_name="to_cvu", on_delete=models.CASCADE)
    cash_sended = models.CharField(max_length=50, default="")
    cash_losed = models.CharField(max_length=50, default="")
    date = models.CharField(max_length=60, default="")

class Transactions(models.Model):
    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE, default=None)
    cash_moved = models.CharField(max_length=50, default="")
    type_of_move = models.CharField(max_length=50, default="")
    date = models.CharField(max_length=60, default="")
