from django.contrib import admin
from .models import Emprestimo

# Register your models here.
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
  list_display = ('livro', 'usuario', 'data_retirada', 'data_prevista_devolucao', 'status')
  list_filter = ('status',)
  search_fields = ('livro__titulo', 'usuario__username')