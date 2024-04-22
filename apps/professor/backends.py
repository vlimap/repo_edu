# apps/professor/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AdminEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if request and request.path.startswith('/admin'):
            try:
                user = UserModel.objects.get(email=username)
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            except UserModel.DoesNotExist:
                return None
        return super().authenticate(request, username, password, **kwargs)
