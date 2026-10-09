from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import RegistroUsuarioForm, LoginUsuarioForm

class RegistroUsuarioView(CreateView):
  form_class = RegistroUsuarioForm
  template_name = 'users/signup.html'
  success_url = reverse_lazy('login')

class LoginUsuarioView(LoginView):
  form_class = LoginUsuarioForm
  template_name = 'users/login.html'
  # success_url = reverse_lazy('login')
  # Debido a que definimos LOGIN_REDIRECT_URL en settings.py,
  # no necesitamos definir success_url.