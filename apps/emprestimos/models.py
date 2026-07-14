from django.db import models
from django.conf import settings
from catalogo.models import Livro

# Create your models here.
class Emprestimo(models.Model):
  STATUS_CHOICES = [
    ('ativo', 'Ativo'),
    ('devolvido', 'Devolvido'),
    ('atrasado', 'Atrasado')
  ]

  usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='emprestimos'
  )
  livro = models.ForeignKey(
    Livro,
    on_delete=models.CASCADE,
    related_name='emprestimos'
  )
  data_retirada = models.DateTimeField(auto_now_add=True)
  data_prevista_devolucao = models.DateField()