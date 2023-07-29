from django.db import models

class Banking(models.Model):
    user = models.ForeignKey("Perfiles.Cuenta", on_delete=models.CASCADE)
    cvu = models.CharField(max_length=22, unique=True, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"Billetera de {self.user.get_full_name()}"

class Transferencias(models.Model):
    sender = models.ForeignKey("Perfiles.Cuenta", on_delete=models.CASCADE, related_name='sent_transferencias')
    receiver = models.ForeignKey("Perfiles.Cuenta", on_delete=models.CASCADE, related_name='received_transferencias')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

class Transactions(models.Model):
    user = models.ForeignKey("Perfiles.Cuenta", on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_ingreso = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)