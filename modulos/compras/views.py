from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import MateriaPrima, Proveedor, StockMateriaPrima, Pago
from .forms import MateriaPrimaForm, StockMateriaPrimaForm, ProveedorForm


# Vistas Materia Prima
from ..accounts.decorators import allowed_users


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


class StockMateriaPrimaListView(ListView, LoginRequiredMixin):
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
    template_name = 'proveedores_add.html'
    success_url = reverse_lazy('compras:proveedor_list')

@method_decorator(allowed_users('compras.view_proveedor'), name='dispatch')
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'proveedores_list.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prov in self.get_queryset():
                    proveedor = {}
                    proveedor['ruc'] = prov.ruc
                    proveedor['razon_social'] = prov.razon_social
                    proveedor['telefono'] = prov.telefono
                    proveedor['email'] = prov.email
                    proveedor['direccion'] = prov.direccion
                    proveedor['id'] = prov.id
                    data.append(proveedor)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {}
            context['title'] = 'Proveedores'
            context['subtitle'] = 'Lista de Proveedores'
            context['route'] = reverse_lazy('compras:proveedor_list')
            context['form'] = ProveedorForm()
            return render(request, self.template_name, context)

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    # template_name=
    success_url = reverse_lazy()


class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
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
