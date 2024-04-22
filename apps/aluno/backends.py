from django.contrib.auth.backends import ModelBackend
from apps.aluno.models import Aluno
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Aluno.objects.get(email=username)
            if user.check_password(password):
                return user
        except Aluno.DoesNotExist:
            return None
