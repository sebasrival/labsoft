from django import forms
from modulos.produccion.models import Equipo, FormulaProducto, OrdenElaboracion, Producto
from datetime import datetime

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
            'stock_inicial': forms.NumberInput(attrs={'class': 'form-control','min':1}),

        }


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
  
        }




class OrdenElaboracionForm(forms.ModelForm):
    class Meta:
        model = OrdenElaboracion
        fields = '__all__'
        widgets = {
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_modificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_teorica': forms.NumberInput(attrs={'class': 'form-control','min':1}),
            'aprobado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'verificado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'elaborado_por': forms.TextInput(attrs={'class': 'form-control'}),

            'fecha_emision': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'fecha_vigencia': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
        }



class FormulaForm(forms.ModelForm):
    class Meta:
        model = FormulaProducto
        fields = '__all__'
        widgets = {
            'producto': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_teorica': forms.TextInput(attrs={'class': 'form-control'}),
  
        }