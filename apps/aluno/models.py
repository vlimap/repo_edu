from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class AlunoManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # A senha é criptografada aqui
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not password:
            raise ValueError('Superusers must have a password.')
        return self.create_user(email, password, **extra_fields)

class Aluno(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='Nome Completo')
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        validators=[RegexValidator(regex=r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$')],
        verbose_name='CPF'
    )
    foto = models.ImageField(upload_to=f'fotos/%Y/%m/%d/', blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now, verbose_name='Data de Cadastro')
    registration_ip = models.GenericIPAddressField(verbose_name='IP de Cadastro', default='0.0.0.0')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = AlunoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cpf']

    def __str__(self):
        return self.email
