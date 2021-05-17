from django import forms

from modulos.ventas.models import Cobro, Cuota, FacturaVenta,Cliente


class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = '__all__'
        widgets = {
            'metodo_cobro': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cobro': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_cuotas': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = '__all__'
        widgets = {
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_cuota': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control'}),
        }


class FacturaVentaForm(forms.ModelForm):
    class Meta:
        model = FacturaVenta
        fields = '__all__'
        widgets = {
            'tipo_venta': forms.TextInput(attrs={'class': 'form-control'}),
            'monto_iva1': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_iva2': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),

        }

