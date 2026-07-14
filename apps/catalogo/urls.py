from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('livro/novo/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro, name='editar_livro'),
    path('livro/<int:livro_id>/deletar/', views.deletar_livro, name='deletar_livro')
]