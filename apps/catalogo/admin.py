from django.contrib import admin
from .models import Autor, Livro
from emprestimos.models import Emprestimo

class EmprestimoInline(admin.TabularInline):
  model = Emprestimo
  extra = 0
  fields = ('usuario', 'data_prevista_devolucao', 'status')
  readonly_fields = ('data_prevista_devolucao',)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
  list_display = ('nome', 'nacionalidade')
  search_fields = ('nome',)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
  list_display = ('titulo', 'autor', 'ano_publicacao', 'disponivel')
  list_filter = ('disponivel', 'ano_publicacao')
  search_fields = ('titulo', 'isbn')
  inlines = [EmprestimoInline]
  autocomplete_fields = ['autor']