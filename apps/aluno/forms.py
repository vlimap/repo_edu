from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
from apps.aluno.models import Aluno

class FormLogin(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'})
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )

class FormCadastro(forms.ModelForm):
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}),
        required=True
    )

    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'email', 'password', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormCadastro, self).__init__(*args, **kwargs)
        

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Aluno.objects.filter(cpf=cpf).exists():
            raise ValidationError('Este CPF já está cadastrado.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Aluno.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'As senhas não são iguais.')
        return cleaned_data

class AtualizarPerfil(UserChangeForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'email', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control read-only', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control read-only', 'readonly': 'readonly'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

    password = forms.CharField(
        label='Nova Senha (deixe em branco para manter a atual)',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite nova senha, se desejar alterar'}),
        required=False
    )

    password_confirmation = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a nova senha'}),
        required=False
    )

    def clean_cpf(self):
        # CPF é somente leitura, então podemos apenas retornar o valor sem validações adicionais
        return self.cleaned_data.get('cpf')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')
        
        # Verifica se ambos os campos de senha foram preenchidos para tentar alterar a senha
        if password and password != password_confirmation:
            self.add_error('password_confirmation', 'As senhas não correspondem.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Altera a senha apenas se uma nova foi fornecida
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user