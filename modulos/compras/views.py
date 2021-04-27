from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import MateriaPrima, Proveedor, StockMateriaPrima, Pago
from .forms import MateriaPrimaForm, StockMateriaPrimaForm, ProveedorForm


# Vistas Materia Prima
class MateriaPrimaCreateView(CreateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    # template_name=
    success_url = reverse_lazy()


class MateriaPrimaListView(ListView):
    model = MateriaPrima


class MateriaPrimaUpdateView(UpdateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    # template_name=
    success_url = reverse_lazy()


class MateriaPrimaDeleteView(DeleteView):
    model = MateriaPrima
    # template_name=
    success_url = reverse_lazy()


# Vistas de Stock de Materia Prima
class StockMateriaPrimaCreateView(CreateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm
    # template_name=
    success_url = reverse_lazy()


class StockMateriaPrimaListView(ListView):
    model = StockMateriaPrima


class StockMateriaUpdateView(UpdateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm
    # template_name_suffix = '_update_form'
    # success_url=


class StockMateriaPrimaDeleteView(DeleteView):
    model = StockMateriaPrima
    # template_name=
    success_url = reverse_lazy()


# Vistas de Proveedores
class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm


class ProveedorListView(ListView):
    model = Proveedor


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    # template_name=
    success_url = reverse_lazy()


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    # template_name=
    success_url = reverse_lazy()


# Vistas de Pagos
class PagoCreateView(CreateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm
    # template_name=
    success_url = reverse_lazy()


class PagoListView(ListView):
    model = Pago


class PagoUpdateView(UpdateView):
    model = Pago
    form_class = MateriaPrimaForm
    # template_name=
    success_url = reverse_lazy()


class PagoDeleteView(DeleteView):
    model = Pago
    # template_name=
    success_url = reverse_lazy()
