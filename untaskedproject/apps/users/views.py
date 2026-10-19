from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import RegistroUsuarioForm, LoginUsuarioForm

class RegistroUsuarioView(CreateView):
  form_class = RegistroUsuarioForm
  template_name = 'users/signup.html'
  success_url = reverse_lazy('login')

  def form_valid(self, form):
      try:
            # Garantiza que si algo falla dentro, NADA se guarde en la BD
            with transaction.atomic():
              response = super().form_valid(form)
              return response
      except Exception as e:
         return self.form_invalid(form)

class LoginUsuarioView(LoginView):
  form_class = LoginUsuarioForm
  template_name = 'users/login.html'
  # success_url = reverse_lazy('login')
  # Debido a que definimos LOGIN_REDIRECT_URL en settings.py,
  # no necesitamos definir success_url.