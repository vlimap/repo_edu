from django.urls import path
from apps.professor.views import home, login_view_professor, edit_profile_professor, logout_professor
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('login-view-professor', login_view_professor, name='login-professor'),
    path('edit-profile-professor', edit_profile_professor, name='edit-professor'),
    path('logout-professor', logout_professor, name='logout-professor'),
]
