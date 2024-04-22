from django.shortcuts import render, redirect
from apps.professor.forms import AtualizarPerfil, LoginForm  
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'aluno/home.html')

def login_view_professor(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matricula = form.cleaned_data.get('matricula')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=matricula, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Seja bem-vindo!')
                    return redirect('home')  # Assegure-se de que 'home' está corretamente definido em suas URLs
                else:
                    messages.error(request, 'Esta conta está desativada.')
            else:
                messages.error(request, 'Matrícula ou senha incorretos.')
    else:
        form = LoginForm()
    return render(request, 'professor/login.html', {'form': form})

@login_required
def edit_profile_professor(request):
    if request.method == 'POST':
        form = AtualizarPerfil(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('home')  
    else:
        form = AtualizarPerfil(instance=request.user)
    return render(request, 'professor/edit-profile.html', {'form': form})

@login_required
def logout_professor(request):
    logout(request)
    messages.success(request, 'Você foi deslogado com sucesso!')
    return redirect('login-professor')  
