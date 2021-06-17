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

from .models import MateriaPrima, Proveedor, StockMateriaPrima, Pago, FacturaCompra, FacturaDet
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
                    item = {'id': prov.id, 'text': prov.razon_social}
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
                        'text': '%s | %s' % (mat.codigo, mat.nombre),  # para el select
                        'codigo': mat.codigo,
                        'desc': mat.descripcion,
                        'nombre': mat.nombre,
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

    # noinspection DuplicatedCode
    def post(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            try:
                with transaction.atomic():
                    # Factura
                    fc = json.loads(request.POST['factura_compra'])
                    factura = FacturaCompra()

                    factura.proveedor = Proveedor.objects.get(id=fc['proveedor'])
                    factura.nro_factura = fc['nro_factura']
                    factura.fecha_factura = datetime.strptime(fc['fecha_factura'], '%d/%m/%Y')
                    factura.tipo_factura = fc['tipo_compra']
                    factura.descuento = fc['descuento']
                    factura.monto_iva1 = fc['totalIva5']
                    factura.monto_iva2 = fc['totalIva10']
                    factura.total = fc['total_compra']

                    pago = Pago()
                    pago.metodo_pago = fc['metodo_pago']
                    pago.descripcion = fc['descripcion_pago']
                    pago.save()
                    factura.pago = pago

                    if FacturaCompra.objects.filter(nro_factura=factura.nro_factura).exists():
                        raise Exception('El número ' + factura.nro_factura + ' de factura ya existe')
                    factura.save()

                    # Factura Detalle
                    for f in fc['materias']:
                        det = FacturaDet()
                        print(f)
                        det.factura = factura
                        if MateriaPrima.objects.filter(codigo=f['codigo']).exists():
                            materia = MateriaPrima.objects.get(codigo=f['codigo'])
                            det.materia = materia
                            #  traemos el stock para actualizar
                            stock = StockMateriaPrima.objects.get(materia=materia)
                            stock.cantidad += f['cantidad']
                            stock.save()
                        else:
                            # si no existe se crea la materia prima
                            mat = MateriaPrima(codigo=f['codigo'],
                                               nombre=f['nombre'],
                                               descripcion=f['desc'],
                                               inci=f['inci'],
                                               um=f['um'],
                                               cantidadCont=f['cantidadCont'])
                            mat.save()
                            # se crea la materia prima antes y luego se guarda en stock
                            stock = StockMateriaPrima(materia=mat, cantidad=f['cantidad'])
                            stock.save()
                            det.materia = mat
                        det.cantidad = f['cantidad']
                        det.precio = f['precio']
                        det.descripcion = f['nombre']
                        det.tipo_iva = f['iva']
                        det.save()
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


class FacturaCompraListView(LoginRequiredMixin, ListView):
    model = FacturaCompra
    template_name = 'factura/factura_list.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaCompraListView, self).get_context_data(**kwargs)
        context['title'] = 'Factura Compra'
        context['subtitle'] = 'Lista de Facturas Compra'
        context['route'] = reverse_lazy('compras:factura_list')
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for f in self.get_queryset():
                    factura = {
                        'nro_factura': f.nro_factura,
                        'tipo_factura': 'Contado' if f.tipo_factura else 'Credito',
                        'fecha_factura': f.fecha_factura,
                        'estado': f.estado,
                        'pago': f.pago.metodo_pago,
                        'total': f.total,
                        'id': f.id,
                    }
                    data.append(factura)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            return super().get(self, request, *args, **kwargs)


class FacturaCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = FacturaCompra
    form_class = FacturaCompraForm
    template_name = 'factura/factura_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Factura Compra'
        context['subtitle'] = 'Editar Factura Compra'
        context['route'] = reverse_lazy('compras:factura_edit', kwargs={'pk': self.get_object().id})
        context['form_mat'] = MateriaPrimaForm
        context['detalle_fact'] = json.dumps(self.get_detalle_fact())
        context['form_pago'] = PagoForm(instance=self.get_object().pago)
        return context

    # noinspection DuplicatedCode
    def post(self, request, *args, **kwargs):
        data = {}
        if request.is_ajax():
            try:
                with transaction.atomic():
                    # Factura
                    fc = json.loads(request.POST['factura_compra'])
                    # Traemos de nuevo el obj factura
                    factura = FacturaCompra.objects.get(id=self.get_object().id)
                    factura.proveedor = Proveedor.objects.get(id=fc['proveedor'])
                    factura.nro_factura = fc['nro_factura']
                    factura.fecha_factura = datetime.strptime(fc['fecha_factura'], '%d/%m/%Y')
                    factura.tipo_factura = fc['tipo_compra']
                    factura.descuento = fc['descuento']
                    factura.monto_iva1 = fc['totalIva5']
                    factura.monto_iva2 = fc['totalIva10']
                    factura.total = fc['total_compra']

                    pago = Pago.objects.get(id=factura.pago.id)
                    pago.metodo_pago = fc['metodo_pago']
                    pago.descripcion = fc['descripcion_pago']
                    pago.save()
                    factura.save()

                    # se vuelve al stock anterior
                    for f in FacturaDet.objects.filter(factura=factura):
                        if StockMateriaPrima.objects.filter(materia=f.materia).exists() == True:
                            materia = MateriaPrima.objects.get(id=f.materia.id)
                            stock = StockMateriaPrima.objects.get(materia=materia)
                            print(stock)
                            stock.cantidad = stock.cantidad - f.cantidad

                    factura.facturadet_set.all().delete()
                    # Factura Detalle
                    for f in fc['materias']:
                        det = FacturaDet()
                        print(f)
                        det.factura = factura
                        if MateriaPrima.objects.filter(codigo=f['codigo']).exists() == True:
                            materia = MateriaPrima.objects.get(codigo=f['codigo'])
                            det.materia = materia
                            #  traemos el stock para actualizar
                            if StockMateriaPrima.objects.filter(materia__codigo=f['codigo']).exists() == True:
                                stock = StockMateriaPrima.objects.get(materia=materia)
                                stock.cantidad += f['cantidad']
                                stock.save()
                        else:
                            # si no existe se crea la materia prima
                            mat = MateriaPrima(codigo=f['codigo'],
                                               nombre=f['nombre'],
                                               descripcion=f['desc'],
                                               inci=f['inci'],
                                               um=f['um'],
                                               cantidadCont=f['cantidadCont'])
                            mat.save()
                            # se crea la materia prima antes y luego se guarda en stock
                            stock = StockMateriaPrima(materia=mat, cantidad=f['cantidad'])
                            stock.save()
                            det.materia = mat
                        det.cantidad = f['cantidad']
                        det.precio = f['precio']
                        det.descripcion = f['nombre']
                        det.tipo_iva = f['iva']
                        det.save()
                    data['message'] = 'La factura ha sido editado correctamente!'
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

    def get_detalle_fact(self):
        data = []
        try:
            for f in FacturaDet.objects.filter(factura=self.get_object().id):
                print(f.tipo_iva)
                data.append(
                    {
                        'codigo': f.materia.codigo,
                        'nombre': f.materia.nombre,
                        'cantidad': int(f.cantidad),
                        'precio': float(f.precio),
                        'iva': int(f.tipo_iva),
                        'id': f.materia.id
                    }
                )
            return data
        except Exception as e:
            raise(str(e))


class FacturaCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = FacturaCompra
    success_url = reverse_lazy('compras:factura_list')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            # agregar para eliminar pagos
            return super().delete(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('compras:factura_list')



# Vistas de Stock de Materia Prima
class StockMateriaPrimaCreateView(LoginRequiredMixin, CreateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm
    template_name = 'stock/stock_materia_add.html'
    success_url = reverse_lazy('compras:stock_list')
    # permission_required = 'compras.add_proveedor'

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
            return redirect('compras:stock_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('compras:stock_list')


class StockMateriaPrimaListView(LoginRequiredMixin, ListView):
    model = StockMateriaPrima
    template_name = 'stock/stock_materia_list.html'
    # permission_required = 'compras.view_proveedor'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for st in self.get_queryset():
                    stock_materia = {
                        'materia': st.materia.nombre,
                        'cantidad': st.cantidad,
                        'id': st.id
                    }
                    data.append(stock_materia)
                    print(stock_materia)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'Stock Compras',
                'subtitle': 'Stock Materia Prima',
                'route': reverse_lazy('compras:stock_list'),
                'form': StockMateriaPrimaForm()
            }
            return render(request, self.template_name, context)


class StockMateriaUpdateView(LoginRequiredMixin, UpdateView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm
    template_name = 'stock/stock_materia_edit.html'
    # success_url = reverse_lazy('compras:proveedor_list')
    # permission_required = 'compras.change_proveedor'
    # url_redirect = reverse_lazy('index')

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
            return redirect('compras:stock_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('compras:proveedor_list')


class StockMateriaPrimaDeleteView(LoginRequiredMixin, DeleteView):
    model = StockMateriaPrima
    form_class = StockMateriaPrimaForm
    success_url = reverse_lazy('compras:stock_list')
    # permission_required = 'compras.delete_proveedor'
    url_redirect = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('compras:stock_list')

