from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def bibliotecario_required(view_func):
  """
  Permite o acesso à view apenas para usuários com o tipo 'bibliotecario'.
  Usuários não logados são redirecionados para o login (via login_required).
  Usuários logados mas sem permissão recebem 403 Forbidden.
  """
  @login_required
  @wraps(view_func)
  def wrapper(request, *args, **kwargs):
    if request.user.tipo != 'bibliotecario':
      raise PermissionDenied
    return view_func(request, *args, **kwargs)
  return wrapper