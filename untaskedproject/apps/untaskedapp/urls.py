from django.urls import path
from .views import CursoListView, TareaListView, CursoCreateView, TareaCreateView, TareaDeleteView, CursoDeleteView

urlpatterns = [
  path('cursos/', CursoListView.as_view(), name='mis_cursos'),
  path('tareas/', TareaListView.as_view(), name='mis_tareas'),
  path('cursos/crear/', CursoCreateView.as_view(), name='crear_curso'),
  path('tareas/crear/', TareaCreateView.as_view(), name='crear_tarea'),
  path('tareas/<int:pk>/eliminar', TareaDeleteView.as_view(), name='eliminar_tarea'),
  path('cursos/<int:pk>/eliminar', CursoDeleteView.as_view(), name='eliminar_curso'),
]
