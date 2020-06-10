from datetime import datetime

from django.forms import *
from .models import Pedido, PedidoDetalle


class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['estado']
        widgets = {
            'cliente': Select(attrs={'class': 'form-control',
                                     'id': 'cliente_select',
                                     'style': 'width: 100%',}),
            'fecha_entrega': DateInput(attrs={'class': 'form-control',
                                              'id': 'datePick',
                                              'placeholder': 'Selecciona la fecha a entregar',
                                              'style': 'font-weight: bold;',
                                              'autocomplete': 'off'}),
            'fecha_pedido': DateInput(attrs={
                'class': 'form-control',
                'value': datetime.now(),
            })
        }


class PedidoDetalleForm(ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'})
        }
