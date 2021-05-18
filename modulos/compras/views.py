from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import MateriaPrima, Proveedor, StockMateriaPrima, Pago
from .forms import MateriaPrimaForm, StockMateriaPrimaForm, ProveedorForm

from ..accounts.decorators import allowed_users


# Vistas de Proveedores
from ..accounts.mixins import PermissionMixin


class ProveedorCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/proveedores_add.html'
    success_url = reverse_lazy('compras:proveedor_list')
    permission_required = 'compras.add_proveedor'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            response = ''
            try:
                form = self.get_form()
                # noinspection DuplicatedCode
                if form.is_valid():
                    form.save()
                    data['message'] = f'¡{self.model.__name__} registrado correctamente!'
                    data['error'] = '¡Sin errores!'
                    response = JsonResponse(data, safe=False)
                    response.status_code = 201  # codigo de que esta bien
                else:
                    data['message'] = '¡Los datos ingresados no son validos!'
                    data['error'] = form.errors
                    response = JsonResponse(data, safe=False)
                    response.status_code = 400  # codigo de que hay algo malo xd
            except Exception as e:
                data['error'] = str(e)
            return response
        else:
            return redirect('compras:proveedor_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('compras:proveedor_list')


class ProveedorListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Proveedor
    template_name = 'proveedores/proveedores_list.html'
    permission_required = 'compras.view_proveedor'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prov in self.get_queryset():
                    proveedor = {
                        'ruc': prov.ruc,
                        'razon_social': prov.razon_social,
                        'telefono': prov.telefono,
                        'email': prov.email,
                        'direccion': prov.direccion,
                        'id': prov.id
                    }
                    data.append(proveedor)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'Proveedores',
                'subtitle': 'Lista de Proveedores',
                'route': reverse_lazy('compras:proveedor_list'),
                'form': ProveedorForm()
            }
            return render(request, self.template_name, context)


class ProveedorUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/proveedores_edit.html'
    #success_url = reverse_lazy('compras:proveedor_list')
    permission_required = 'compras.change_proveedor'
    url_redirect = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            response = ''
            try:
                form = self.form_class(request.POST, instance=self.get_object())
                # noinspection DuplicatedCode
                if form.is_valid():
                    form.save()
                    data['message'] = f'¡{self.model.__name__} editado correctamente!'
                    data['error'] = '¡Sin errores!'
                    response = JsonResponse(data, safe=False)
                    response.status_code = 201  # codigo de que esta bien
                else:
                    data['message'] = '¡Los datos ingresados no son validos!'
                    data['error'] = form.errors
                    response = JsonResponse(data, safe=False)
                    response.status_code = 400  # codigo de que hay algo malo xd
            except Exception as e:
                data['error'] = str(e)
            return response
        else:
            return redirect('compras:proveedor_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('compras:proveedor_list')


class ProveedorDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy('compras:proveedor_list')
    permission_required = 'compras.delete_proveedor'
    url_redirect = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('compras:proveedor_list')


# Vistas Materia Prima
class MateriaPrimaCreateView(CreateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm


class MateriaPrimaListView(ListView):
    model = MateriaPrima


class MateriaPrimaUpdateView(UpdateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm


class MateriaPrimaDeleteView(DeleteView):
    model = MateriaPrima
    success_url = reverse_lazy()


# Vistas de Stock de Materia Prima
class StockMateriaPrimaCreateView(CreateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm


class StockMateriaPrimaListView(ListView, LoginRequiredMixin):
    model = StockMateriaPrima


class StockMateriaUpdateView(UpdateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm


class StockMateriaPrimaDeleteView(DeleteView):
    model = StockMateriaPrima


# Vistas de Pagos
class PagoCreateView(CreateView):
    model = MateriaPrima
    form_class = MateriaPrimaForm


class PagoListView(ListView):
    model = Pago


class PagoUpdateView(UpdateView):
    model = Pago
    form_class = MateriaPrimaForm


class PagoDeleteView(DeleteView):
    model = Pago
