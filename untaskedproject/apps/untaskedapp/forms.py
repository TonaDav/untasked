from django import forms
from datetime import date
from .models import Curso, Tarea, Subtarea
from django.forms import inlineformset_factory

"""
class CursoForm(forms.ModelForm):
  class Meta:
    model = Curso
    fields = ['nombre']
    labels = {
      'nombre':'Curso'
    }
    widgets = {
      'nombre': forms.TextInput(attrs={
        'class':'form-control',
      })
    }

class TareaForm(forms.ModelForm):
  class Meta:
    model = Tarea
    fields = ['descripcion','curso','fecha_limite','prioridad']
    labels = {
      'descripcion':'Descripción',
      'curso':'Curso',
      'fecha_limite':'Fecha límite',
      'prioridad':'Prioridad',
    }

    widgets = {
      'descripcion': forms.TextInput(attrs={
        'class':'form-control'
      }),
      'curso': forms.Select(attrs={
        'class':'form-select'
      }),
      'fecha_limite': forms.DateInput(attrs={
        'class':'form-control',
        'type':'date',
      }),
      'prioridad': forms.Select(attrs={
        'class':'form-select'
      })
    }

  def __init__(self, *args, **kwargs):

    # Extraemos del diccionario kwargs el parámetro usuario.
    # Debemos extraer y quitar usuario de kwargs antes de llamar
    # a __init__() porque el método no reconoce el argumento usuario.
    usuario = kwargs.pop('usuario', None)

    # Llamos al constructor original de
    # ModelForm para que construya el formulario.
    super().__init__(*args, **kwargs)

    # Filtramos los cursos por usuario.
    if usuario:
      self.fields['curso'].queryset = Curso.objects.filter(usuario=usuario)

  # Nos aseguramos que fecha_limite sea válido.
  def clean_fecha_limite(self):
    fecha_limite = self.cleaned_data.get('fecha_limite')

    if fecha_limite and fecha_limite < date.today():
      raise forms.ValidationError('La fecha límite no puede ser pasada.')

    return fecha_limite

class SubtareaForm(forms.ModelForm):
  class Meta:
    model = Subtarea
    fields = ['descripcion']
    widgets = {
      'descripcion': forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Agrega una subtarea...',
      })
    }

# Utilizamos FormSets cuando queremos crear múltiples instancias
# del mismo formulario dentro de una misma página HTML.
# inlineformset_factory es utilizado cuando tenemos una relación padre-hijo.
# En este caso, Tarea es el padre y Subtarea el hijo (1:N).
SubtareaCreateFormSet = inlineformset_factory(
  Tarea, # Padre
  Subtarea, # Hijo
  form=SubtareaForm,
  extra=3, # Cuántos formularios tenemos al principio
  can_delete=False,
)

SubtareaUpdateForm = inlineformset_factory(
  Tarea,
  Subtarea,
  form=SubtareaForm,
  extra=1,
  can_delete=True,
)
"""
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

SubtareaUpdateFormset = inlineformset_factory(
  parent_model=Tarea,
  model=Subtarea,
  form=SubtareaForm,
  extra=3,
  can_delete=True
)