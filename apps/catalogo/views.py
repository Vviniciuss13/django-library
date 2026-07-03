from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def lista_livros(request):
    """
    View responsável por exibir a lista de livros do acervo.
    Por enquanto, retorna um texto simples de teste.
    """
    return HttpResponse("Bem-vindo ao catálogo da biblioteca")

def detalhe_livro(request, livro_id):
    """
    View responsável por exibir os detalhes de um livro específico.
    Por enquanto, apenas confirma o ID recebido via URL.
    """
    return HttpResponse(f"Detalhes do livro com ID: {livro_id}")