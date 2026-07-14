from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
  path('solicitar/<int:livro_id>/', views.solicitar_emprestimo, name='solicitar_emprestimo'),
  path('meus/', views.meus_emprestimos, name='meus_emprestimos'),
  path('devolver/<int:emprestimo_id>/', views.devolver_emprestimo, name='devolver_emprestimo'),
]