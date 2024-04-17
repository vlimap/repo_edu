from django.urls import path
from .views import home, login_view, signup_view, logout_view,  edit_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login', login_view, name='login'),
    path('cadastro', signup_view, name='signup'),
    path('logout', logout_view, name='logout'),
    path('editar-perfil', edit_profile, name='edit_profile'),
]
