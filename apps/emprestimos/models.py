from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

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
  data_devolucao = models.DateField(null=True, blank=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
  
  class Meta:
    ordering = ['-data_retirada']
    verbose_name = 'Empréstimo'
    verbose_name_plural = 'Empréstimos'

  def __str__(self):
    return f"{self.livro.titulo} - {self.usuario.username}"
  
  def save(self, *args, **kwargs):
    if not self.data_prevista_devolucao:
      self.data_prevista_devolucao = timezone.now().date() + timedelta(days=7)
    super().save(*args, **kwargs)