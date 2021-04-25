from django import forms
from .models import Proveedores,Pago,MateriaPrima,StockMateriaPrima


class ProveedorForm(forms.ModelForm):
    class Meta():
        model = Proveedores
        fields = '__all__'
        widgets = {
            'ruc' : forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
            'direccion' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class PagoForm(forms.ModelForm):
    class Meta():
        model = Pago
        fields = '__all__'
        widgets = {
            'metodo_pago' : forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class MateriaPrimaForm(forms.ModelForm):
    class Meta():
        model = MateriaPrima
        fields = '__all__'
        widgets = {
            'cod_materia' : forms.TextInput(attrs={'class': 'form-control'}),
            'nombre ' : forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class': 'form-control'}),
            'inci ' : forms.TextInput(attrs={'class': 'form-control'}),
            'um' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class StockMateriaPrimaForm(forms.ModelForm):
    class Meta():
        model = MateriaPrima
        fields = '__all__'
        widgets = {
            'cod_materia' : forms.TextInput(attrs={'class': 'form-control'}),
            'nombre ' : forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion' : forms.TextInput(attrs={'class': 'form-control'}),
            'inci ' : forms.TextInput(attrs={'class': 'form-control'}),
            'um' : forms.TextInput(attrs={'class': 'form-control'}),
        }

