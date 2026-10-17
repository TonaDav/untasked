from .models import Curso, Tarea
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CursoForm, TareaForm, SubtareaCreateFormset

class CursoListView(LoginRequiredMixin, ListView):
  model = Curso
  context_object_name = 'cursos'
  template_name = 'untaskedapp/cursos.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form'] = CursoForm()
    return context

  # Modificamos el método get_queryset() responsable de realizar
  # la consulta SQL, obteniendo solo los cursos del usuario logueado.
  def get_queryset(self):
    usuario = self.request.user
    return Curso.objects.filter(usuario=usuario)

class CursoCreateView(LoginRequiredMixin, CreateView):
  model = Curso
  form_class = CursoForm
  success_url = reverse_lazy('mis_cursos')

  # form_valid() se ejecuta después de que todos los datos ingresados
  # han sido validados exitosamente. Nos permite agregar datos adicionales
  # al objeto en memoria antes de que super().form_valid(form) guarde el objeto permanentemente en la BD.
  def form_valid(self, form):
    usuario = self.request.user
    # self.instance representa al objeto creado por el formulario
    # (en este caso un curso) que aún no ha sido registrado en el database.
    # Aquí le asignamos un usuario (el que está logueado), pues no puede haber un curso sin usuario.
    form.instance.usuario = usuario
    return super().form_valid(form)

class TareaListView(LoginRequiredMixin, ListView):
  model = Tarea
  context_object_name = 'tareas'

  # Sobreescribimos el método get_queryset() para evitar que
  # traiga todas las tareas de la base de datos. En su lugar,
  # le ordenamos que solo traiga las tareas del usuario logeuado.
  def get_queryset(self):
    usuario = self.request.user
    return Tarea.objects.filter(curso__usuario=usuario).select_related('curso').prefetch_related('subtareas')

  # Necesitamos este méotdo para que cuando abramos el modal
  # de agregar tarea, el formulario modal tenga los inputs correspondientes
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Pasamos el formulario Tarea inyectándole el usuario logueado.
    context['form'] = TareaForm(usuario=self.request.user)
    # Pasamos el formset de creación de subtareas para el modal.
    context['subtarea_formset'] = SubtareaCreateFormset()
    return context

class TareaCreateView(LoginRequiredMixin, CreateView):
  model = Tarea
  form_class = TareaForm
  success_url = reverse_lazy('mis_tareas')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['usuario'] = self.request.user
    return kwargs

  def form_valid(self, form):
    subtarea_formset = SubtareaCreateFormset(self.request.POST)

    if subtarea_formset.is_valid():
      with transaction.atomic():
        self.object = form.save()
        subtarea_formset.instance = self.object
        subtarea_formset.save()
      return redirect(self.get_success_url())
    return self.form_invalid(form=form, subtarea_formset=subtarea_formset)