from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from catalogo.models import Livro
from .models import Emprestimo

# Create your views here.
@login_required
def solicitar_emprestimo(request, livro_id):
  """Permite que um usuário logado solicite o empréstimo de um livro disponível."""
  livro = get_object_or_404(Livro, pk=livro_id)

  if not livro.disponivel:
    messages.error(request, 'Este livro não está disponível para empréstimo no momento')
    return redirect('catalogo:detalhe_livro', livro_id=livro.id)

  if request.method == 'POST':
    Emprestimo.objects.create(usuario=request.user, livro=livro)
    livro.disponivel = False
    livro.save()
    messages.success(request, f'Emprestimo de "{livro.titulo}" realizado com sucesso!')
    return redirect('emprestimos:meus_emprestimos')
  
  return render(request, 'emprestimos/confirmar_emprestimo.html', {'livro': livro})

@login_required
def meus_emprestimos(request):
  """Lista todos os empréstimos do usuário logado."""
  emprestimos = Emprestimo.objects.filter(usuario=request.user)
  return render(request, 'emprestimos/meus_emprestimos.html', {'emprestimos': emprestimos})

@login_required
def devolver_emprestimo(request, emprestimo_id):
  """Permite ao usuário logado devolva o livro emprestado"""
  emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id, usuario=request.user)

  if emprestimo.status == 'devolvido':
    messages.warning(request, 'Este empréstimo já foi devolvido anteriormente.')
    return redirect('emprestimos:meus_emprestimos')

  if request.method == 'POST':
    emprestimo.status = 'devolvido'
    emprestimo.data_devolucao = timezone.now()
    emprestimo.save()

    emprestimo.livro.disponivel = True
    emprestimo.livro.save()

    messages.success(request, f'Devolução de "{emprestimo.livro.titulo}" registrada com sucesso!')
    return redirect('emprestimos:meus_emprestimos')

  return render(request, 'emprestimos/confirmar_devolucao.html', {'emprestimo': emprestimo})
