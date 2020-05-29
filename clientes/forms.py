from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta():
        model = Cliente
        fields = '__all__'
        widgets = {
            'id_documento' : forms.TextInput(attrs={'class': 'form-control'}),
            'es_entidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
            'apellido' : forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social' : forms.TextInput(attrs={'class': 'form-control'}),
            'descuento' : forms.NumberInput(attrs={'class': 'form-control'}),
            'bonificacion' : forms.NumberInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
            'direccion' : forms.TextInput(attrs={'class': 'form-control'}),
        }