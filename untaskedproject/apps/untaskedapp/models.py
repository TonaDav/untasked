from datetime import date
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Validamos la fecha límite a nivel de Modelo
# para evitar que alguien en el Admin Dashboard
# o en la consola de Python ingrese una fecha inválida.
def validate_fecha_limite(fecha_limite):
  if fecha_limite < date.today():
    raise ValidationError('La fecha límite no debe ser pasada.')

class Curso(models.Model):
  usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cursos')
  nombre = models.CharField(max_length=50)

  def __str__(self):
    return f'{self.nombre}'

class Tarea(models.Model):
  PRIORIDADES = [
    ('BAJA', 'Baja'),
    ('MEDIA', 'Media'),
    ('ALTA', 'Alta'),
    ('URGENTE', 'Urgente'),
  ]

  curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='tareas')
  descripcion = models.CharField(max_length=50)
  fecha_limite = models.DateField(validators=[validate_fecha_limite])
  prioridad = models.CharField(choices=PRIORIDADES, max_length=8, default='BAJA')

  def __str__(self):
    return f'{self.descripcion}'

class Subtarea(models.Model):
  tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='subtareas')
  descripcion = models.CharField(max_length=150)

  def __str__(self):
    return f'{self.descripcion}'