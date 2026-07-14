from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.LivroListView.as_view(), name='lista_livros'),
    path('livro/<int:livro_id>/', views.LivroDetailView.as_view(), name='detalhe_livro'),
    path('livro/novo/', views.LivroCreateView.as_view(), name='cadastrar_livro'),
    path('livro/<int:livro_id>/editar/', views.LivroUpdateView.as_view(), name='editar_livro'),
    path('livro/<int:livro_id>/deletar/', views.LivroDeleteView.as_view(), name='deletar_livro')
]