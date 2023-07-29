from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from banking.models import Banking
from utils.generar_cvu import generar_cvu

class CuentaManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, born_date, phone, dni, province, city, address, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not born_date:
            raise ValueError("User must have a born date")
        if not phone:
            raise ValueError("User must have a phone")
        if not dni:
            raise ValueError("User must have a dni")
        if not address:
            raise ValueError("User must have an address")
        if not province:
            raise ValueError("User must have a province")
        if not city:
            raise ValueError("User must have a city")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            born_date = born_date,
            phone = phone,
            dni = dni,
            address = address,
            province = province,
            city = city,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, born_date, phone, dni, city, province, address, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            born_date = born_date,
            phone = phone,
            dni = dni,
            address = address,
            province = province,
            city = city,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Cuenta(AbstractBaseUser):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=60, unique=True)
    born_date = models.DateField(auto_now=False, default=None, null=True, blank=True)
    phone = models.CharField(max_length=14, default="")
    dni = models.CharField(max_length=8, default="")
    province = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=250, default="")
    address = models.CharField(max_length=140, default="")
    date_joined = models.DateField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'born_date', 'phone', 'city', 'dni', 'address', 'province']

    objects = CuentaManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=get_user_model())
def user_created(sender, instance, created, **kwargs):
    if created:
        banking = Banking()
        banking.user = instance
        banking.cvu = generar_cvu()
        banking.save()

post_save.connect(user_created, sender=get_user_model())