from django.db import models
from django.contrib.auth import get_user
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Writing an email is mandatory!'))

        email = self.normalize_email(email)
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

    def permision_observer(self, email, password, **extra_fields):
        extra_fields.setdefault('is_observer', True)

        if not extra_fields.get("is_observer"):
            raise ValueError(_(f'The user must have is_observer=True.'))


class User(AbstractUser):
    full_name = models.CharField(_('full name'), max_length=256, blank=True, null=True)
    email = models.EmailField(_('email addres'), unique=True, blank=False, null=False)
    phone_number = models.CharField(_('phone number'), max_length=11, blank=True, null=True)
    is_supervisor = models.BooleanField(_('supervisor'), default=False)
    is_observer = models.BooleanField(_('observer'), default=False)
    is_operator = models.BooleanField(_('operator'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'
