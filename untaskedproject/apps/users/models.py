from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UsuarioManager(BaseUserManager):

  # Nos permite crear usuarios comunes.
  def create_user(self, email, username, password=None, **extra_fields):
    # Verificamos que el email exista.
    if not email:
      raise ValueError('El correo electrónico es obligatorio.')

    # Verificamos que el username exista.
    if not username:
      raise ValueError('El nombre de usuario es obligatorio.')

    # Estandarizamos el correo: ToNa10@GMAIL.com → tona10@gmail.com
    email = self.normalize_email(email)
    # Guardamos el usuario en memoria.
    user = self.model(email=email, username=username, **extra_fields)
    # Le asignamos la contraseña.
    user.set_password(password)
    # Lo guardamos en la base de datos.
    user.save(using=self._db)
    return user

  # Nos permite crear superusuarios.
  def create_superuser(self, email, username, password=None, **extra_fields):
    # Verificamos que los campos sean verdaderos.
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_superuser', True)

    # Verificamos.
    if extra_fields.get('is_staff') is not True:
      raise ValueError("El superusuario debe ser is_staff.")
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('El superusuario debe ser is_superuser.')

    return self.create_user(email, username, password, **extra_fields)

class Usuario(AbstractUser):

  email = models.EmailField('correo electrónico', unique=True, error_messages={
    'unique': ('Este correo electrónico ya está en uso.'),
  })
  username = models.CharField('nombre de usuario', max_length=30, unique=True, error_messages={
    'unique': ('Este nombre de usuario ya está en uso.'),
  })

  # Indicamos a Django que use a email como el identificador para el inicio de sesión.
  USERNAME_FIELD = 'email'

  # Definimos el campo username como campo obligatorio.
  # Por defecto, ya tenemos los campos email y password.
  # Por eso, solo colocamos username en REQUIRED_FIELDS.
  REQUIRED_FIELDS = ['username']

  # Vinculamos nuestro UsuarioManager de tal manera que
  # cuando llamemos a Usuario.objects.create() usemos la lógica de email.
  objects = UsuarioManager()

  def __str__(self):
    return f'{self.email}'

  def save(self,  *args, **kwargs):
    if self.email:
      self.email = self.email.strip().lower()
    super().save(*args, **kwargs)
