from django.contrib import admin
from .models import Aluno

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'cpf', 'registration_date', 'is_active', 'is_superuser')
    list_display_links = ('email', 'name')
    search_fields = ('name', 'email', 'cpf')
    list_filter = ('is_superuser', 'is_active', 'registration_date')
    list_editable = ('is_active',)

admin.site.register(Aluno, AlunoAdmin)
