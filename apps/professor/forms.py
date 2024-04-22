from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from apps.professor.models import Professor

class LoginForm(forms.Form):
    matricula = forms.CharField(
        label=_("Matrícula"),
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matrícula'}),
    )
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
    )

    def clean(self):
        matricula = self.cleaned_data.get('matricula')
        password = self.cleaned_data.get('password')

        if matricula and password:
            user = authenticate(username=matricula, password=password)
            if user is None:
                raise forms.ValidationError(_("Matrícula ou senha incorretos."))
            if not user.is_active:
                raise forms.ValidationError(_("Esta conta está desativada."))
        return self.cleaned_data
    
class AtualizarPerfil(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['nome', 'email', 'foto', 'cpf']
        labels = {
            'nome': _('Nome Completo'),
            'email': _('Email'),
            'foto': _('Foto'),
            'cpf': _('CPF'),
        }
        help_texts = {
            'nome': _('Informe seu nome completo.'),
            'email': _('Informe seu endereço de email.'),
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'nome': {
                'max_length': _("Este nome é muito longo."),
            },
            'email': {
                'invalid': _("Insira um endereço de email válido."),
            }
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Professor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Um usuário com este email já existe."))
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        return cpf
