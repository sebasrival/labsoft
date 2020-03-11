from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta():
        model = Producto
        fields = '__all__'
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'volumen': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_neto': forms.NumberInput(attrs={'class': 'form-control'}),
        }
