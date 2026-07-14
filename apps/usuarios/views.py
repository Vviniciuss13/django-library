from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CadastroForm

# Create your views here.
def cadastro(request):
  """Cadastra um novo usuário e já efetua o login automaticamente."""
  if request.method == 'POST':
    form = CadastroForm(request.POST)
    if form.is_valid():
      usuario = form.save()
      login(request, usuario)
      return redirect('catalogo:lista_livros')
  else:
    form = CadastroForm()
  
  return render(request, 'usuarios/cadastro.html', {'form': form})