from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import FormLogin, FormCadastro, AtualizarPerfil
from .models import Aluno
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'aluno/home.html')

def login_view(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password) 
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Seja bem-vindo!')
                    return redirect('home')
                else:
                    messages.error(request, 'Esta conta está desativada.')
            else:
                messages.error(request, 'E-mail ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FormLogin()
    return render(request, 'aluno/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        # Incluindo request.FILES para processar o upload de arquivos
        form = FormCadastro(request.POST, request.FILES)
        if form.is_valid():
            # Use form.save() diretamente, já que o ModelForm pode lidar com isso
            aluno = form.save(commit=False)  # Salva o objeto Aluno mas não comita ainda para o DB
            aluno.set_password(form.cleaned_data['password'])
            aluno.save()  # Agora comita as mudanças para o banco de dados

            messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça login.')
            return redirect('login')  # Redireciona para a página de login
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FormCadastro()
    
    return render(request, 'aluno/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta com sucesso.')
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = AtualizarPerfil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('home')
    else:
        form = AtualizarPerfil(instance=request.user)
    
    return render(request, 'aluno/edit_profile.html', {'form': form})