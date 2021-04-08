from datetime import datetime

from django.forms import *
from .models import Factura, FacturaDetalle


class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        exclude = ['estado']
        widgets = {
            'nro_factura': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nro de factura'
            }),
            'cliente': Select(attrs={'class': 'form-control',
                                     'id': 'cliente_select',
                                     'style': 'width: 100%', }),
            'fecha_emision': DateInput(attrs={'class': 'form-control',
                                              'id': 'datePick-emision',
                                              'placeholder': 'Selecciona la fecha de emision',
                                              'style': 'font-weight: bold;',
                                              'autocomplete': 'off'}),
        }


class FacturaDetalle(ModelForm):
    class Meta:
        model = FacturaDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'})
        }
