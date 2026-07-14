from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
  class Meta:
    model = Livro
    fields = ['titulo', 'autor', 'isbn', 'ano_publicacao', 'disponivel', 'capa']
    widgets = {
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'isbn': forms.TextInput(attrs={'class': 'form-control'}),
      'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
    }