from django import forms
from .models import Proveedor, Pago, MateriaPrima, StockMateriaPrima



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
class ProductoForm(forms.ModelForm):
    class Meta():
        model = Producto
        fields = '__all__'
        widgets = {
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Textarea(attrs={'class': 'form-control'}),
            'volumen': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_contenido': forms.NumberInput(attrs={'class': 'form-control'}),
        }

