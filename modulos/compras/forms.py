from django import forms
from .models import Proveedor, Pago, MateriaPrima, StockMateriaPrima, FacturaCompra, FacturaDet


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows':2}),
            'cantidadCont': forms.NumberInput(attrs={'class': 'form-control', 'min':1}),
            'inci': forms.TextInput(attrs={'class': 'form-control'}),
            'um': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StockMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = StockMateriaPrima
        fields = '__all__'
        widgets = {
            'cod_materia': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FacturaCompraForm(forms.ModelForm):
    class Meta:
        model = FacturaCompra
        exclude = ['estado', 'pago']
        widgets = {
            'nro_factura' : forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'off'}),
            'proveedor': forms.Select(attrs={'class': 'form-control',
                                                'id': 'proveedor_select',
                                                'style': 'width: 100%; '}),
            'fecha_factura': forms.DateInput(attrs={
                'class': 'form-control',
                'id':'date_compra',
                'style': 'font-weight: bold;',
                'autocomplete': 'off',
            }),
            'tipo_factura' : forms.RadioSelect(choices=((True, 'Contado',), (False, 'Credito',))),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step':5}),
        }

class FacturaDetalleCompraForm(forms.ModelForm):
    class Meta:
        model = FacturaDet
        fields = ['materia', 'cantidad']
        widgets = {
            'materia': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
        }