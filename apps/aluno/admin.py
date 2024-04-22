from django.contrib import admin
from apps.aluno.models import Aluno

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'cpf', 'data_de_cadastro', 'is_active', 'is_superuser') 
    list_display_links = ('email', 'nome')  
    search_fields = ('nome', 'email', 'cpf')  
    list_filter = ('is_superuser', 'is_active', 'data_de_cadastro') 
    list_editable = ('is_active',)

admin.site.register(Aluno, AlunoAdmin)
