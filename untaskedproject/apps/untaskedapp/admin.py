from django.contrib import admin
from .models import Curso, Tarea, Subtarea

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
  list_display = ['nombre', 'usuario']
  list_filter = ['usuario']

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
  list_display = ['descripcion', 'fecha_limite', 'prioridad', 'is_completada', 'curso']
  list_filter = ['curso__usuario']

@admin.register(Subtarea)
class SubtareaAdmin(admin.ModelAdmin):
  list_display = ['descripcion', 'is_completada', 'tarea']