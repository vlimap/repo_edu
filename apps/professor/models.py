from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class ProfessorManager(BaseUserManager):
    def create_user(self, matricula, password=None, **extra_fields):
        if not matricula:
            raise ValueError(_('A matrícula é obrigatória'))
        user = self.model(matricula=matricula, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not password:
            raise ValueError(_('Superusuários devem ter uma senha.'))
        return self.create_user(matricula, password, **extra_fields)

class Professor(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    nome = models.CharField(max_length=100, verbose_name=_('Nome Completo'))
    cpf = models.CharField(max_length=14, unique=True, verbose_name=_('CPF'))
    matricula = models.CharField(max_length=20, unique=True, verbose_name=_('Matrícula'))
    foto = models.ImageField(upload_to='fotos_professores/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Foto'))
    data_de_cadastro = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    ip_de_cadastro = models.GenericIPAddressField(default='0.0.0.0', verbose_name=_('IP de Cadastro'))
    is_active = models.BooleanField(default=True, verbose_name=_('Ativo'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Equipe'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superusuário'))

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='grupos_professor',
        blank=True,
        help_text=_('Os grupos aos quais este usuário pertence. Um grupo representa uma coleção de permissões.'),
        verbose_name=_('Grupos')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permissoes_usuario_professor',
        blank=True,
        help_text=_('Permissões específicas para este usuário.'),
        verbose_name=_('Permissões de Usuário')
    )

    objects = ProfessorManager()

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['nome', 'cpf', 'email']
    
    @property
    def is_professor(self):
        return True

    def __str__(self):
        return self.matricula

    class Meta:
        verbose_name = _('Professor')
        verbose_name_plural = _('Professores')
