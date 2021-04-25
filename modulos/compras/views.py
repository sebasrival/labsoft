from django.shortcuts import render
from django.views.generic.edit import CreateView,ListView
from compras.models import MateriaPrima,Proveedores,StockMateriaPrima,Pago
from compras.forms import MateriaPrimaForm


#Vistas Materia Prima
class MateriaPrimaCreateView(CreateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class MateriaPrimaListView(ListView):
    model = MateriaPrima
    template_name='compra/listado_materia_prima.html'

class MateriaPrimaUpdateView(UpdateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class MateriaPrimaDeleteView(DeleteView):
    model = MateriaPrima
    #template_name=
    success_url=reverse_lazy()
#Vistas de Stock de Materia Prima
class StockMateriaPrimaCreateView(CreateView):
    model = StockMateriaPrima
    form_class=StockMateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class StockMateriaPrimaListView(ListView):
    model = StockMateriaPrima
    template_name='compra/listado_stock_materia_prima.html'

class StockMateriaUpdateView(UpdateView):
    model = StockMateriaPrima
    form_class=StockMateriaPrimaForm
    #template_name_suffix = '_update_form'
    #success_url=

class StockMateriaPrimaDeleteView(DeleteView):
    model = StockMateriaPrima
    #template_name=
    success_url=reverse_lazy()

#Vistas de Proveedores
class ProveedorCreateView(CreateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()


class ProveedorListView(ListView):
    model = Proveedores
    template_name='compra/listado_proveedores.html'

class ProveedorUpdateView(UpdateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class ProveedorDeleteView(DeleteView):
    model = Proveedores
    #template_name=
    success_url=reverse_lazy()

#Vistas de Pagos 
class PagoCreateView(CreateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class PagoListView(ListView):
    model = Pago
    template_name='compra/listado_pagos.html'

class PagoUpdateView(UpdateView):
    model = MateriaPrima
    form_class=MateriaPrimaForm
    #template_name=
    success_url=reverse_lazy()

class PagoDeleteView(DeleteView):
    model = MateriaPrima
    #template_name=
    success_url=reverse_lazy()