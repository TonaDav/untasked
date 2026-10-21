from django import forms
from .models import Usuario
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistroUsuarioForm(UserCreationForm):
  class Meta:
    model = Usuario
    fields = ['email','username']
    labels = {
      'email':'Correo electrónico',
      'username':'Nombre de usuario',
    }
    widgets = {
      'email': forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'correo@ejemplo.com'
      }),
      'username': forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Tu nombre de usuario'
      })
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['password1'].label = 'Contraseña'
    self.fields['password2'].label = 'Confirma tu contraseña'

    self.fields['password1'].widget = forms.PasswordInput(attrs={
      'class':'form-control',
      'placeholder':'Mínimo 8 caracters'
    })
    self.fields['password2'].widget = forms.PasswordInput(attrs={
      'class':'form-control',
      'placeholder':'Repite tu contraseña'
    })

    # Quitamos los textos de ayuda a los campos de contraseña.
    self.fields['password1'].help_text = None
    self.fields['password2'].help_text = None

    # Modificamos el mensaje de validación de longitud de ambos campos.
    self.fields['password1'].validators.append(
            MinLengthValidator(
                8,
                message=(
                    'La contraseña es demasiado corta. Debe contener al menos 8 caracteres.'
                ),
            )
        )
    self.fields['password2'].validators.append(
                MinLengthValidator(
                    8,
                    message=(
                        'La contraseña es demasiado corta. Debe contener al menos 8 caracteres.'
                    ),
                )
            )

class LoginUsuarioForm(AuthenticationForm):
  username = forms.EmailField(
    label='Correo electrónico',
    widget= forms.EmailInput(attrs={
      'class':'form-control',
      'placeholder':'correo@ejemplo.com'
    })
  )
  password = forms.CharField(
    label='Contraseña',
    widget= forms.PasswordInput(attrs={
      'class':'form-control',
      'placeholder':'*****'
    })
  )

  def clean_username(self):
    username = self.cleaned_data.get('username')
    if username:
      return username.strip().lower()
    return username