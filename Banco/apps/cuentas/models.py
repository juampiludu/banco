from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.banking.models import Banking
from utils.generar_cvu import generar_cvu
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin


class CuentaManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()

        return user

class Cuenta(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=60, unique=True)
    born_date = models.DateField(auto_now=False, null=True)
    phone = models.CharField(max_length=14, null=True)
    dni = models.CharField(max_length=8, unique=True, null=True)
    province = models.CharField(max_length=50, null=True)
    localidad = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=140, null=True)
    date_joined = models.DateField(verbose_name="date joined", default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CuentaManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_privilege(self):
        return self.is_staff and self.is_superuser


@receiver(post_save, sender=get_user_model())
def user_created(sender, instance, created, **kwargs):        
    if created:
        banking = Banking()
        banking.user = instance
        banking.cvu = generar_cvu()
        banking.save()

post_save.connect(user_created, sender=get_user_model())