from django.db import models
from Perfiles.models import Cuenta

class Notification(models.Model):

    user = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    text = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
