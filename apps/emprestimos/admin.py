from django.contrib import admin
from django.utils import timezone
from .models import Emprestimo

# Register your models here.
@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
  list_display = ('livro', 'usuario', 'data_retirada', 'data_prevista_devolucao', 'status')
  list_filter = ('status',)
  search_fields = ('livro__titulo', 'usuario__username')
  actions = ['marcar_como_devolvido']

  @admin.action(description='Marcar empréstimos selecionados como devolvidos')
  def marcar_como_devolvido(self, request, queryset):
    atualizados = queryset.filter(status='ativo').update(
      status='devolvido',
      data_devolucao=timezone.now()
    )
    self.message_user(request, f'{atualizados} empréstimo(s) marcado(s) como devolvido(s).')