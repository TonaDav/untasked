from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegistroUsuarioView, LoginUsuarioView

urlpatterns = [
  path('signup/', RegistroUsuarioView.as_view(), name='signup'),
  path('login/', LoginUsuarioView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout')
  # Debido a que definimos LOGOUT_REDIRECT_URL en settings.py,
  # no necesitamos definir LogoutView.as_view(next_page=)
]