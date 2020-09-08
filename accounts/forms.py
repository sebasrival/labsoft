from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import *

from .models import User


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta():
        model = User
        fiels = ("first_name", "last_name", "email", "username", "groups", "password1", "password2")
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'username': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff', 'password']


class UserFormChange(UserChangeForm):
    password1 = CharField(label="Contraseña",
                                widget=PasswordInput(attrs={
                                    'class':'form-control',
                                }))
    password2 = CharField(label="Confirmar Contraseña",
                                widget=PasswordInput(attrs={
                                        'class': 'form-control',
                                    }
                                ),
                                help_text="Ingrese la misma contraseña que la anterior, para verificación.")
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username","profile","groups",)
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'username': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("La contraseñas no coinciden")
        return password2