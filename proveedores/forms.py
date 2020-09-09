from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta():
        model = Proveedor
        fields = '__all__'
        widgets = {
            'ruc' : forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
            'direccion' : forms.TextInput(attrs={'class': 'form-control'}),
        }