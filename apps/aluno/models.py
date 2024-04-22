from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class AlunoManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O e-mail é obrigatório'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not password:
            raise ValueError(_('Superusuários devem ter uma senha.'))
        return self.create_user(email, password, **extra_fields)

class Aluno(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    nome = models.CharField(max_length=100, verbose_name=_('Nome Completo'))
    cpf = models.CharField(max_length=14, unique=True, verbose_name=_('CPF'))
    foto = models.ImageField(upload_to='fotos/%Y/%m/%d/', blank=True, null=True, verbose_name=_('Foto'))
    data_de_cadastro = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Cadastro'))
    ip_de_cadastro = models.GenericIPAddressField(default='0.0.0.0', verbose_name=_('IP de Cadastro'))
    is_active = models.BooleanField(default=True, verbose_name=_('Ativo'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Equipe'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superusuário'))

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='grupos_aluno',
        blank=True,
        help_text=_('Os grupos aos quais este usuário pertence. Um grupo representa uma coleção de permissões.'),
        verbose_name=_('Grupos')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permissoes_usuario_aluno',
        blank=True,
        help_text=_('Permissões específicas para este usuário.'),
        verbose_name=_('Permissões de Usuário')
    )

    objects = AlunoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    @property
    def is_professor(self):
        return False

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Aluno')
        verbose_name_plural = _('Alunos')

class Post(models.Model):
    author = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to=f'post/%Y/%m/%d/', blank=True, null=True) 
    links = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    class Meta:
        ordering = ['-created_at'] 
