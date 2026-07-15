from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBibliotecarioOrReadOnly(BasePermission):
  """
  Permite leitura (GET, HEAD, OPTIONS) para qualquer usuário autenticado.
  Permite escrita (POST, PUT, PATCH, DELETE) apenas para Bibliotecarios.
  """
  message = 'Apenas bibliotecarios podem realizar essa ação'

  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    return bool(
      request.user
      and request.user.is_authenticated
      and request.user.tipo == 'bibliotecario'
    )