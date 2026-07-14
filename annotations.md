# Learning Django

## Starting

First of all, you need to install the django and create a venv to isolate the dependencies of your project, to do this you can use the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django
```

## Structure

The framework django is structured by a project with apps, so, one project has many apps inside

## Project

The configuration for project is at config folder.

- setting.py: the main configuration of project
- urls.py: the index of routes

## Apps

The apps is inside of a folder named apps, in the apps has some file:

- admin.py: This file configure the admin painel with the models
- forms.py: This file add the forms of app (register, login, ...)
- models.py: Register the models of app, this models reflect the db's tables
- urls.py: This file configure the routes of app
- views.py: This file has the logic of app, this file is responsible for the requests and responses

### Admin

```python
@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
  list_display = ('titulo', 'autor', 'ano_publicacao', 'disponivel')
  list_filter = ('disponivel', 'ano_publicacao')
  search_fields = ('titulo', 'isbn')
```

### Form

```python
class LivroForm(forms.ModelForm):
  class Meta:
    model = Livro
    fields = ['titulo', 'autor', 'isbn', 'ano_publicacao', 'disponivel']
    widgets = {
      'titulo': forms.TextInput(attrs={'class': 'form-control'}),
      'isbn': forms.TextInput(attrs={'class': 'form-control'}),
      'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
    }
```

### Model

```python
class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='livros'
    )
    isbn = models.CharField(max_length=13, unique=True)
    ano_publicacao = models.IntegerField()
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return self.titulo
```

### Url

```python
app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('livro/<int:livro_id>/', views.detalhe_livro, name='detalhe_livro'),
    path('livro/novo/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro, name='editar_livro'),
    path('livro/<int:livro_id>/deletar/', views.deletar_livro, name='deletar_livro')
]
```

### View

```python
def cadastrar_livro(request):
    """Exibe e processa o formulário de cadastro de um novo livro"""
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalogo:lista_livros')
    else:
        form = LivroForm()
    
    return render(request, 'catalogo/cadastrar_livro.html', {'form': form})
```

## Migrations

The migrations are the files that reflect the changes in the models, this files are created by the command:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Templates

The templates are the files that are responsible for the front-end of the project, this files are created inside of a folder named templates, and this folder is inside of the app's folder. You can reuse the templates by using the {% include %} tag, and you can extend the templates by using the {% extends %} tag.

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Biblioteca{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{% url 'catalogo:lista_livros' %}">Início</a>
        <a href="{% url 'catalogo:cadastrar_livro' %}">Cadastrar Livro</a>
    
        {% if user.is_authenticated %}
          <span>Olá, {{ user.username }}!</span>
          <form method="post" action="{% url 'usuarios:logout' %}" style="display: inline;">
            {% csrf_token %}
            <button type="submit">Sair</button>
          </form>
        {% else %}
          <a href="{% url 'usuarios:login' %}">Login</a>
          <a href="{% url 'usuarios:cadastro' %}">Cadastro</a>
        {% endif %}
    </nav>

    <hr>

    {% block content %}
    {% endblock %}

</body>
</html>
```

```html
{% extends "base.html" %}

{% block title %}{{ livro.titulo }}{% endblock title %}

{% block content %}
  <h1>{{ livro.titulo }}</h1>
  <p>Autor: {{ livro.autor.nome }}</p>
  <p>Ano de Publicação: {{ livro.ano_publicacao }}</p>
  <p>Disponível: {% if livro.disponivel %}Sim{% else %}Não{% endif %}</p>
  
  <a href="{% url 'catalogo:editar_livro' livro.id %}">Editar</a>
  <a href="{% url 'catalogo:deletar_livro' livro.id %}">Excluir</a>
  <a href="{% url 'catalogo:lista_livros' %}">Voltar ao catálogo</a>
{% endblock content %}
```

## Custom User Auth

You can create a custom user model by extending the AbstractUser class, and you can create a custom user form by extending the UserCreationForm class. You can also create a custom user view to handle the registration of new users.

```python
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
```

## Decorators

There are some decorators that you can use to restrict access to views, like @login_required and @permission_required. You can also create your own decorators to restrict access based on user type.

```python
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
```

## Images and Files

- Use the libary Pillow to check the images
- Configure the settings.py

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

- In model:

```python
models.ImageField(upload_to='capas_livros/', blank=True, null=True) 
```

- Form need to be enctype multipart/form-data

- In view pass in form class the request files

```python
form = LivroForm(request.POST, request.FILES)
```

Obs: It's not recommend use urls.py to show files, it's slow, use nginx for example
