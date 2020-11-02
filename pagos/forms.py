from django import forms
from .models import Pago,PagoCuota
from datetime import datetime

class PagoForm(forms.ModelForm):
    class Meta():
        model = Pago
        fields = '__all__'

        widgets = {
            'cedula' : forms.TextInput(attrs={'class': 'form-control'}),
            'nro_factura' : forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_pago' : forms.DateInput(attrs={
                'class': 'form-control',
                'value': datetime.now().strftime('%d/%m/%Y'),
            }),
            'metodo_pago': forms.Select(attrs={'class': 'form-control',
                                     'id': 'metodo_pago_select',
                                     'style': 'width: 100%',}),
           'estado': forms.Select(attrs={'class': 'form-control',
                                     'id': 'estado_select',
                                     'style': 'width: 100%',}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control',
                                     'id': 'tipo_pago_select',
                                     'style': 'width: 100%',}),
            'monto_total' : forms.NumberInput(attrs={'class': 'form-control'}),
             'cantidad_cuotas' : forms.NumberInput(attrs={'class': 'form-control'}),
            'es_contado' : forms.CheckboxInput(),
            'es_cliente' : forms.CheckboxInput(),
        }
class PagoCuotaForm(forms.ModelForm):
        class Meta():
            model = PagoCuota
            fields = '__all__'
            widgets = {
                'id_pago': forms.NumberInput(attrs={'class': 'form-control'}),
                'fecha_pago' : forms.DateInput(attrs={
                'class': 'form-control'
                }),
                'fecha_vencimiento' : forms.DateInput(attrs={
                'class': 'form-control'
             }),
                'estado': forms.Select(attrs={'class': 'form-control',
                                     'id': 'estado_select',
                                     'style': 'width: 100%',}),
        
                'monto_cuota' : forms.NumberInput(attrs={'class': 'form-control'}),
             }