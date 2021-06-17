from django import forms
from modulos.produccion.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'volumen': forms.NumberInput(attrs={'class': 'form-control','min':1}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control','min':1}),
            'cantidad_contenido': forms.NumberInput(attrs={'class': 'form-control','min':1}),
            'tasa_iva': forms.Select(attrs={'class': 'form-control'}),
        }



