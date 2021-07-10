from django import forms

class ReporteFiltro(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'autocomplete':'off'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'autocomplete':'off'}))

class MesForm(forms.Form):
    mes = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'autocomplete':'off'}))
