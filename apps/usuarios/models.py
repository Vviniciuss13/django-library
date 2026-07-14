from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Usuario(AbstractUser):
  """
  Usuário customizado do sistema.
  Herda username, password, email, first_name, last_name do AbstractUser
  """
  TIPO_CHOICES = [
    ('leitor', 'Leitor'),
    ('bibliotecario', 'Bibliotecário'),
  ]

  tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='leitor')
  telefone = models.CharField(max_length=20, blank=True)

  def __str__(self):
    return self.username
  
