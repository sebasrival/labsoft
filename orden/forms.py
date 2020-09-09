from datetime import datetime

from django import forms


# Create your froms here.
from orden.models import OrdenElaboracion


class OrdenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    class Meta:
        model = OrdenElaboracion
        fields = '__all__'
        exclude = ['hora_inicio', 'hora_final']
        widgets = {
            'desc_producto': forms.Textarea(attrs={
                'class':'form-control'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'value': datetime.now().strftime('%d/%m/%Y')
            }),
        }