import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import MateriaPrima, Proveedor, StockMateriaPrima, Pago, FacturaCompra
from .forms import MateriaPrimaForm, StockMateriaPrimaForm, ProveedorForm, FacturaCompraForm, PagoForm
from ..accounts.mixins import PermissionMixin


# Proveedores

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
    # success_url = reverse_lazy('compras:proveedor_list')
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


class SearchProveedor(TemplateView):
    """Clase para buscar proveedor por ajax y devielvo un JsonResponse"""
    def get(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            try:
                term = request.GET['term']
                query = Proveedor.objects.filter(Q(razon_social__icontains=term) | Q(ruc__icontains=term))[0:10]
                data = []
                for prov in query:
                    item = {'id': prov.ruc, 'text': prov.razon_social}
                    data.append(item)
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = 'Solo se admiten peticiones ajax'
        return JsonResponse(data, safe=False)


class SearchMateriaPrima(TemplateView):
    """Clase para buscar materia prima por ajax y devielvo un JsonResponse"""
    def get(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            try:
                term = request.GET['term']
                query = MateriaPrima.objects.filter(Q(codigo__icontains=term) | Q(nombre__icontains=term))[0:10]
                data = []
                for mat in query:
                    item = {
                        'id': mat.id,
                        'text': '%s | %s' % (mat.codigo, mat.nombre), # para el select
                        'codigo': mat.codigo,
                        'nombre': mat.descripcion,
                        'inci': mat.inci,
                        'um': mat.um,
                        'cantidadCont': mat.cantidadCont
                    }
                    data.append(item)
            except Exception as e:
                data['error'] = str(e)
        else:
            data['error'] = 'Solo peticiones ajax'
        return JsonResponse(data, safe=False)


# Factura
class FacturaCompraCreateView(LoginRequiredMixin, CreateView):
    model = FacturaCompra
    form_class = FacturaCompraForm
    template_name = 'factura/factura_add.html'

    def post(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            try:
                with transaction.atomic():
                    # Factura
                    fc = json.loads(request.POST['factura_compra'])
                    factura = FacturaCompra()

                    factura.proveedor = Proveedor.objects.get(ruc=fc['proveedor'])
                    factura.nro_factura = fc['nro_factura']
                    factura.fecha_factura = datetime.strptime(fc['fecha_factura'], '%d/%m/%Y')
                    factura.tipo_factura = fc['tipo_compra']
                    factura.descuento = fc['descuento']
                    factura.monto_iva1 =fc['totalIva5']
                    factura.monto_iva2 = fc['totalIva10']
                    factura.total = fc['total_compra']

                    pago = Pago()
                    pago.metodo_pago = fc['metodo_pago']
                    pago.descripcion = fc['descripcion_pago']
                    pago.save()

                    factura.pago = pago
                    if FacturaCompra.objects.filter(nro_factura=factura.nro_factura).exists():
                        raise Exception('El número '+ factura.nro_factura +' de factura ya existe')
                    factura.save()

                    # Factura Detalle

                    data['message'] = 'La factura se ha registrado agregado correctamente!'
                    data['error'] = '¡Sin errores!'
                    response = JsonResponse(data, safe=False)
                    response.status_code = 201
            except Exception as e:
                data['error'] = str(e)
                response = JsonResponse(data, safe=False)
                response.status_code = 400
            return response
        else:
            return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura Compra'
        context['subtitle'] = 'Registrar Factura Compra'
        context['route'] = reverse_lazy('compras:factura_add')
        context['form_mat'] = MateriaPrimaForm
        context['form_pago'] = PagoForm
        return context


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
