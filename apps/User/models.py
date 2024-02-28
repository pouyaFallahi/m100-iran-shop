from django.db import models
from django.contrib.auth import get_user
from django.utils.translation import gettext_lazy as _
from ..Main.models import GeneralManager
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Writing an email is mandatory!'))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get("is_active"):
            raise ValueError(_("Superuser must have is_active=True."))
        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, GeneralManager):
    full_name = models.CharField(_('full name'), max_length=256, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone_number = models.CharField(_('phone number'), max_length=11, blank=True, null=True)
    address = models.CharField(_('address'), max_length=256, blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
