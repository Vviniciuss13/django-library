from django.test import TestCase
from django.urls import reverse

from .models import Autor, Livro
from usuarios.models import Usuario

class LivroModelTest(TestCase):
  def setUp(self):
    """Executado antes de cada CADA método de teste desta classe"""
    self.autor = Autor.objects.create(nome="Machado de Assis")
    self.livro = Livro.objects.create(
        titulo="Dom Casmurro",
        autor=self.autor,
        isbn="9788535910663",
        ano_publicacao=1899
    )
    self.bibliotecario = Usuario.objects.create_user(
      username="bibliotecario", password="senha123", tipo="bibliotecario"
    )
    self.leitor = Usuario.objects.create_user(
      username="leitor", password="senha123", tipo="leitor"
    )
  
  def test_lista_livros_acessivel_sem_login(self):
    """A listagem de livros deve ser pública."""
    response = self.client.get(reverse('catalogo:lista_livros'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Dom Casmurro")

  def test_cadastrar_livro_bloqueado_para_anonimo(self):
      """Usuário não logado deve ser redirecionado ao tentar cadastrar."""
      response = self.client.get(reverse('catalogo:cadastrar_livro'))
      self.assertEqual(response.status_code, 302)

  def test_cadastrar_livro_bloqueado_para_leitor(self):
      """Leitor logado não pode acessar a página de cadastro."""
      self.client.login(username="leitor", password="senha123")
      response = self.client.get(reverse('catalogo:cadastrar_livro'))
      self.assertEqual(response.status_code, 403)

  def test_cadastrar_livro_permitido_para_bibliotecario(self):
      """Bibliotecário logado deve acessar a página de cadastro normalmente."""
      self.client.login(username="bibliotecario", password="senha123")
      response = self.client.get(reverse('catalogo:cadastrar_livro'))
      self.assertEqual(response.status_code, 200)

  def test_str_retorna_titulo(self):
    """O __str__ do livro deve retornar o título."""
    self.assertEqual(str(self.livro), "Dom Casmurro")
  
  def test_livro_disponivel_por_padrao(self):
    """Um livro recém-criado deve estar disponível por padrão."""
    self.assertTrue(self.livro.disponivel)

  def test_livro_vinculado_ao_autor_correto(self):
    """O livro deve aparecer na lista de livros do autor (related_name)."""
    self.assertIn(self.livro, self.autor.livros.all())