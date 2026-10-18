from django import forms
from datetime import date
from .models import Curso, Tarea, Subtarea
from django.forms import inlineformset_factory

class CursoForm(forms.ModelForm):
  class Meta:
    model = Curso
    fields = ['nombre']
    labels = {
      'nombre': 'Nombre',
    }
    widgets = {
      'nombre': forms.TextInput(attrs={
        'class':'form-control',
      })
    }

  def clean_nombre(self):
    nombre = self.cleaned_data.get('nombre')

    if not nombre or not nombre.strip():
      raise forms.ValidationError('El nombre del curso no puede estar en blanco.')

    nombre_clean = nombre.strip()

    return nombre_clean

class TareaForm(forms.ModelForm):
  class Meta:
    model = Tarea
    fields = ['descripcion', 'curso', 'fecha_limite', 'prioridad']
    labels = {
      'descripcion': 'Descripción',
      'curso': 'Curso',
      'fecha_limite': 'Fecha límite',
      'prioridad': 'Prioridad',
    }
    widgets = {
      'descripcion': forms.TextInput(attrs={
        'class':'form-control',
      }),
      'curso': forms.Select(attrs={
        'class':'form-select',
      }),
      'fecha_limite': forms.DateInput(attrs={
        'type':'date',
        'class':'form-control',
      }),
      'prioridad': forms.Select(attrs={
        'class':'form-select',
      })
    }

  def __init__(self, *args, **kwargs):
    # Extraemos del diccionario kwargs el parámetro usuario.
    # Debemos extraer y quitar usuario de kwargs antes de llamar
    # a __init__() porque el método no reconoce el argumento usuario.
    usuario = kwargs.pop('usuario', None)

    # Construimos el formulario.
    super().__init__(*args, **kwargs)

    # Filtramos los cursos por usuario.
    if usuario:
      self.fields['curso'].queryset = Curso.objects.filter(usuario=usuario)

  # Validamos la descripción.
  def clean_descripcion(self):
    descripcion = self.cleaned_data.get('descripcion')

    if not descripcion or not descripcion.strip():
      raise forms.ValidationError('La tarea debe tener una descripción.')

    descripcion_clean = descripcion.strip()

    return descripcion_clean
  
  # Validamos la fecha límite a nivel de Formulario.
  def clean_fecha_limite(self):
    fecha_limite = self.cleaned_data.get('fecha_limite')
    if fecha_limite < date.today():
      raise forms.ValidationError('La fecha límite no debe ser pasada.')
    return fecha_limite

class SubtareaForm(forms.ModelForm):
  class Meta:
    model = Subtarea
    fields = ['descripcion']
    widgets = {
      'descripcion': forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Agregar subtarea...',
      })
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Hacemos el que campo nombre pueda estar vacío
    # para que el formset ignore ese formulario específico.
    self.fields['descripcion'].required = False

# Utilizamos Formsets cuando queremos crear múltiples instancias
# del mismo formulario dentro de una misma página HTML.
# inlineformset_factory es utilizado cuando tenemos una relación padre-hijo.
# En este caso, Tarea es el padre y Subtarea el hijo (1:N).
SubtareaCreateFormset = inlineformset_factory(
  parent_model=Tarea, # Padre
  model=Subtarea, # Hijo
  form=SubtareaForm,
  extra=3, # Número de formularios que tenemos inicialmente
  can_delete=False # No se pueden eliminar subtareas.
)