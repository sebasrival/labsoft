from django import forms
from .models import Pago
from datetime import datetime

class PagoForm(forms.ModelForm):
    class Meta():
        model = Pago
        fields = '__all__'

        widgets = {
            'nro_factura' : forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_pago' : forms.DateInput(attrs={
                'class': 'form-control',
                'value': datetime.now().strftime('%d/%m/%Y'),
            }),
            'metodo_pago': forms.Select(attrs={'class': 'form-control',
                                     'id': 'metodo_pago_select',
                                     'style': 'width: 100%',}),
            'monto_total' : forms.NumberInput(attrs={'class': 'form-control'}),
            'es_contado' : forms.CheckboxInput(),
            'es_cliente' : forms.CheckboxInput(),
        }