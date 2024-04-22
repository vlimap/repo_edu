from django.urls import path
from apps.aluno.views import home, login_view_aluno, edit_profile_aluno,  logout_view_aluno, signup_view_aluno
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login-view-aluno', login_view_aluno, name='login-aluno'),
    path('signup-view-aluno', signup_view_aluno, name='signup-aluno'),
    path('logout-view-aluno', logout_view_aluno, name='logout-aluno'),
    path('edit-profile-aluno', edit_profile_aluno, name='edit-profile-aluno'),
]
