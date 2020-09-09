from django import forms
from .models import Equipo
from datetime import datetime

class EquipoForm(forms.ModelForm):
    class Meta():
        model = Equipo
        fields = '__all__'

        widgets = {
            'codigo_equipo' : forms.TextInput(attrs={'class': 'form-control'}),
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),

            'descripcion' : forms.TextInput(attrs={'class': 'form-control'}),
            'modelo' : forms.TextInput(attrs={'class': 'form-control'}),


            'estado': forms.Select(attrs={'class': 'form-control',
                                     'id': 'estado_select',
                                     'style': 'width: 100%',}),
            'costo' : forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_elaboracion' : forms.TextInput(attrs={'class': 'form-control'})

        }