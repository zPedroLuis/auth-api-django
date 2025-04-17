from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, nome, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    nome = models.CharField(_('nome completo'), max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome'] 

    objects = UserManager()

    def clean(self):
        if not self.email:
            raise ValidationError({'email': _('Este campo é obrigatório.')})
        if len(self.nome) < 3:
            raise ValidationError({'nome': _('O nome deve ter pelo menos 3 caracteres.')})

    def __str__(self):
        return self.email