from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission
from django.forms import *

from .models import User


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['groups'].widget.attrs['class'] = 'group_select'
        self.fields['groups'].widget.attrs['style'] = 'width: 100%'

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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        for grupo in self.cleaned_data['groups']:
            user.groups.add(grupo)
        return user


class UserFormChange(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs['class'] = 'group_select'
        self.fields['groups'].widget.attrs['style'] = 'width: 100%'

    password1 = CharField(required=False,label="Contraseña",
                                widget=PasswordInput(attrs={
                                    'class':'form-control',
                                },))
    password2 = CharField(required=False,label="Confirmar Contraseña",
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

    def save(self, commit=True):
        form = super()
        if form.is_valid():
            user = form.save(commit=False)
            if self.cleaned_data['password1'] != '':
                user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            user.groups.clear()
            for grupo in self.cleaned_data['groups']:
                user.groups.add(grupo)
            return user

    # class GroupForm(ModelForm):
    #
    #     class Meta:
    #         model = Group
    #         fields = '__all__'