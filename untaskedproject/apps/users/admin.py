from .models import Usuario
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Registramos el modelo Usuario en el panel de administración.
# Personalizamos cómo ordernar y qué campos mostrar en la tabla.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
  ordering = ['email']
  list_display = [
    'email',
    'username',
    'first_name',
    'last_name',
    'is_staff',
    'is_active',
  ]

  # Filtros laterales para facilitar la búsqueda en el panel
  list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

  # Campos por lo que se podrá buscar en la barra de búsqueda
  search_fields = ['email', 'username', 'first_name', 'last_name']

  # Estructura del formulario al editar un usuario existente
  fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            'Información Personal',
            {'fields': ('first_name', 'last_name')},
        ),
        (
            'Permisos',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

  # Estructura del formulario al crear un nuevo usuario desde la web
  add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2'), # password1 y password2 para confirmar la constraseña
            },
        ),
    )