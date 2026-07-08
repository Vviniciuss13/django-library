from django.contrib import admin
from .models import Autor, Livro

# Register your models here.
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
  list_display = ('nome', 'nacionalidade')
  search_fields = ('nome',)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
  list_display = ('titulo', 'autor', 'ano_publicacao', 'disponivel')
  list_filter = ('disponivel', 'ano_publicacao')
  search_fields = ('titulo', 'isbn')