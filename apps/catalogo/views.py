from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from usuarios.decorators import bibliotecario_required
from usuarios.permissions import IsBibliotecarioOrReadOnly

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import LivroSerializer

from .models import Livro
from .forms import LivroForm

# VIEWS

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
        form = LivroForm(request.POST, request.FILES)
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
        form = LivroForm(request.POST, request.FILES, instance=livro)
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

# CLASS BASE VIEW
class LivroListView(ListView):
    model = Livro
    template_name = 'catalogo/lista_livros.html'
    context_object_name = 'livros'

class LivroDetailView(DetailView):
    model = Livro
    template_name = 'catalogo/detalhe_livro.html'
    context_object_name = 'livro'
    pk_url_kwarg = 'livro_id'

@method_decorator(bibliotecario_required, name='dispatch')
class LivroCreateView(CreateView):
    model = Livro
    form_class = LivroForm
    template_name = 'catalogo/cadastrar_livro.html'
    success_url = reverse_lazy('catalogo:lista_livros')

@method_decorator(bibliotecario_required, name='dispatch')
class LivroUpdateView(UpdateView):
    model = Livro
    form_class = LivroForm
    template_name = 'catalogo/cadastrar_livro.html'
    pk_url_kwarg = 'livro_id'
    context_object_name = 'livro'

    def get_success_url(self):
        return reverse_lazy('catalogo:detalhe_livro', kwargs={'livro_id': self.object.id})

@method_decorator(bibliotecario_required, name='dispatch')
class LivroDeleteView(DeleteView):
    model = Livro
    template_name = 'catalogo/confirmar_delecao.html'
    pk_url_kwarg = 'livro_id'
    context_object_name = 'livro'
    success_url = reverse_lazy('catalogo:lista_livros')

# VIEW SET (REST)
class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsBibliotecarioOrReadOnly]