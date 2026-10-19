from django.views import View
from .models import Curso, Tarea
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CursoForm, TareaForm, SubtareaCreateFormset
    

class CursoListView(LoginRequiredMixin, ListView):
  model = Curso
  context_object_name = 'cursos'
  template_name = 'untaskedapp/cursos.html'
  paginate_by = 6

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
  template_name = 'untaskedapp/cursos.html'
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

  def form_invalid(self, form):
    # Recuperamos los cursos del usuario para que la lista del fondo no se borre.
    cursos = Curso.objects.filter(usuario=self.request.user)
    return self.render_to_response(
        self.get_context_data(form=form, object_list=cursos)
    )

class CursoDeleteView(LoginRequiredMixin, View):
  def post(self, request, pk):
    curso = get_object_or_404(Curso, pk=pk, usuario=self.request.user)

    if curso.tareas.exists():
      messages.error(request, '¡Este curso tiene tareas relacionadas!')
      return redirect('mis_cursos')

    curso.delete()
    return redirect('mis_cursos')

class TareaListView(LoginRequiredMixin, ListView):
  model = Tarea
  template_name = 'untaskedapp/tareas.html'
  context_object_name = 'tareas'
  paginate_by = 5

  # Sobreescribimos el método get_queryset() para evitar que
  # traiga todas las tareas de la base de datos. En su lugar,
  # le ordenamos que solo traiga las tareas del usuario logeuado.
  def get_queryset(self):
    usuario = self.request.user
    queryset = Tarea.objects.filter(curso__usuario=usuario).select_related('curso').prefetch_related('subtareas')

    filtro = self.request.GET.get('filtro')
    valor = self.request.GET.get('valor')

    if filtro == 'prioridad' and valor:
      queryset = queryset.filter(prioridad=valor.upper())
    elif filtro == 'curso' and valor:
      queryset = queryset.filter(curso_id=valor)

    return queryset.order_by('fecha_limite')

  # Necesitamos este méotdo para que cuando abramos el modal
  # de agregar tarea, el formulario modal tenga los inputs correspondientes
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    usuario = self.request.user
    # Pasamos el formulario Tarea inyectándole el usuario logueado.
    context['form'] = TareaForm(usuario=usuario)
    # Pasamos el formset de creación de subtareas para el modal.
    context['subtarea_formset'] = SubtareaCreateFormset()

    context['cursos_usuario'] = Curso.objects.filter(usuario=usuario)
    context['prioridades_list'] = Tarea.PRIORIDADES
    context['filtro_actual'] = self.request.GET.get('filtro')
    context['valor_actual'] = self.request.GET.get('valor')

    return context

class TareaCreateView(LoginRequiredMixin, CreateView):
  model = Tarea
  form_class = TareaForm
  template_name = 'untaskedapp/tareas.html'
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
        subtareas = subtarea_formset.save(commit=False)

        for subtarea in subtareas:
          if subtarea.descripcion and subtarea.descripcion.strip():
            subtarea.tarea = self.object
            subtarea.save()

      return redirect(self.get_success_url())

    return self.form_invalid(form=form, subtarea_formset=subtarea_formset)

  def form_invalid(self, form, subtarea_formset=None):
    if subtarea_formset is None:
      subtarea_formset = SubtareaCreateFormset(self.request.POST)

    tareas = (
        Tarea.objects.filter(curso__usuario=self.request.user)
        .select_related('curso')
        .prefetch_related('subtareas')
    )

    # Reutilizamos el contexto de la vista ListView pasando la lista de tareas
    context = self.get_context_data(
        form=form,
        subtarea_formset=subtarea_formset,
        tareas=tareas,
        object_list=tareas,
    )
    return self.render_to_response(context)

class TareaDeleteView(LoginRequiredMixin, View):
  def post(self, request, pk):
    # Garantizamos que la tarea pertenezca a un curso del usuario autenticado.
    tarea = get_object_or_404(Tarea, pk=pk, curso__usuario=self.request.user)

    action = request.POST.get('action')

    if action == 'complete':
      messages.success(request, '¡Tarea completada!')

    tarea.delete()
    return redirect('mis_tareas')