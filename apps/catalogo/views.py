from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro
from .forms import LivroForm
from usuarios.decorators import bibliotecario_required

# Create your views here.
def lista_livros(request):
    """Exibe a lista de todos os livros cadastrados no acervo."""
    livros = Livro.objects.all()
    return render(request, 'catalogo/lista_livros.html', {'livros': livros})

def detalhe_livro(request, livro_id):
    """Exibe os detalhes de um livro específico, buscado pelo banco de dados."""
    livro = get_object_or_404(Livro, pk=livro_id)

    return render(request, 'catalogo/detalhe_livro.html', {'livro': livro})

@bibliotecario_required
def cadastrar_livro(request):
    """Exibe e processa o formulário de cadastro de um novo livro"""
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo:lista_livros')
    else:
        form = LivroForm()
    
    return render(request, 'catalogo/cadastrar_livro.html', {'form': form})

@bibliotecario_required
def editar_livro(request, livro_id):
    """Edita um livro existente, reaproveitando o mesmo form de cadastro."""
    livro = get_object_or_404(Livro, pk=livro_id)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('catalogo:detalhe_livro', livro_id=livro.id)
    else:
        form = LivroForm(instance=livro)

    return render(request, 'catalogo/cadastrar_livro.html', {'form': form, 'livro': livro})

@bibliotecario_required
def deletar_livro(request, livro_id):
    """Remove um livro após confirmação do usuário"""
    livro = get_object_or_404(Livro, pk=livro_id)

    if request.method == 'POST':
        livro.delete()
        return redirect('catalogo:lista_livros')
    
    return render(request, 'catalogo/confirmar_delecao.html', {'livro': livro})