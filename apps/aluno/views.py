from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.aluno.forms import FormLogin, FormCadastro, AtualizarPerfil
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'aluno/home.html')

def login_view_aluno(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Verifica se o tipo do usuário corresponde ao selecionado no form
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Seja bem-vindo!')
                    return redirect('home')
                else:
                    messages.error(request, 'Esta conta está desativada.')
            else:
                messages.error(request, 'Tipo de usuário incorreto para esta conta.')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
    else:
        form = FormLogin()
    return render(request, 'aluno/login.html', {'form': form})

def signup_view_aluno(request):
    if request.method == 'POST':
        form = FormCadastro(request.POST, request.FILES)
        if form.is_valid():
                aluno = form.save(commit=False)
                aluno.set_password(form.cleaned_data['password'])
                aluno.save()
                messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça login.')
                return redirect('login-aluno')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FormCadastro()
    
    return render(request, 'aluno/signup.html', {'form': form})

def logout_view_aluno(request):
    logout(request)
    messages.success(request, 'Você saiu da sua conta com sucesso.')
    return redirect('home')

@login_required
def edit_profile_aluno(request):
    if request.method == 'POST':
        form = AtualizarPerfil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('home')
    else:
        form = AtualizarPerfil(instance=request.user)
    
    return render(request, 'aluno/edit_profile.html', {'form': form})