from django.forms import *
from .models import Pedido, PedidoDetalle

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['fecha_pedido']
        widgets = {
            'cliente': Select(attrs={'class':'form-control',
                                     'id': 'cliente_select'}),
            'fecha_entrega': DateInput(attrs={'class': 'form-control',
                                              'id': 'datePick',
                                              'placeholder': 'Selecciona la fecha'}),
            'estado': Select(attrs={'class': 'form-control'})
        }

class PedidoDetalleForm(ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': Select(attrs={'class':'form-control'}),
            'cantidad': NumberInput(attrs={'class':'form-control'})
        } 
