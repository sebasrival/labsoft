from django.forms.forms import Form
from modulos.compras.models import StockMateriaPrima
from django.db.models import Max
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from datetime import datetime
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Vistas de productos
from ..accounts.mixins import PermissionMixin


class ProductoCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_add.html'
    success_url = reverse_lazy('produccion:producto_list')
    permission_required = 'produccion.add_producto'

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
                    p = Producto.objects.get(codigo_producto=form['codigo_producto'].value())
                    s = StockProductos(cantidad=form['stock_inicial'].value(), producto_id=p.id)
                    s.save()
                    print(form)


                else:
                    data['message'] = '¡Los datos ingresados no son validos!'
                    data['error'] = form.errors
                    response = JsonResponse(data, safe=False)
                    response.status_code = 400  # codigo de que hay algo malo xd
            except Exception as e:
                data['error'] = str(e)

            return response
        else:
            return redirect('produccion:producto_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('produccion:producto_list')


class ProductoListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Producto
    template_name = 'productos/productos_list.html'
    permission_required = 'produccion.view_producto'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prod in self.get_queryset():
                    stock = StockProductos.objects.get(producto_id=prod.id)
                    producto = {
                        'codigo_producto': prod.codigo_producto,
                        'nombre': prod.nombre,
                        'tipo': prod.tipo,
                        'color': prod.color,
                        'precio': prod.precio,
                        'cantidad_contenido': prod.cantidad_contenido,
                        'cantidad': stock.cantidad,
                        'id': prod.id
                    }
                    data.append(producto)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'productos',
                'subtitle': 'Stock de productos',
                'route': reverse_lazy('produccion:producto_list'),
                'form': ProductoForm()
            }
            return render(request, self.template_name, context)


class ProductoUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_edit.html'
    success_url = reverse_lazy('produccion:producto_list')
    permission_required = 'produccion.change_producto'

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
            return reverse_lazy('produccion:producto_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:producto_list')


class ProductoDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('produccion:producto_list')
    permission_required = 'produccion.delete_producto'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:producto_list')


# Seccion de equipos.
class EquipoCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Equipo
    form_class = EquipoForm
    template_name = 'equipos/equipos_add.html'
    success_url = reverse_lazy('produccion:equipo_list')
    permission_required = 'produccion.add_equipo'


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
            return redirect('produccion:equipo_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('produccion:equipo_list')


class EquipoListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Equipo
    template_name = 'equipos/equipos_list.html'
    permission_required = 'produccion.view_equipo'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prod in self.get_queryset():
                    equipo = {
                        'codigo': prod.codigo,
                        'nombre': prod.nombre,
                        'id': prod.id
                    }
                    data.append(equipo)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'equipos',
                'subtitle': 'Lista de equipos',
                'route': reverse_lazy('produccion:equipo_list'),
                'form': EquipoForm()
            }
            return render(request, self.template_name, context)


class EquipoUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Equipo
    form_class = EquipoForm
    template_name = 'equipos/equipos_edit.html'
    success_url = reverse_lazy('produccion:equipo_list')
    permission_required = 'produccion.change_equipo'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            response = ''
            try:
                form = self.form_class(request.POST, instance=self.get_object())
                equipo_old=self.get_object()

                # noinspection DuplicatedCode
                if form.is_valid():
                    equipo_edit= form.save(commit=False)
                    if equipo_edit.ultimo_mantenimiento != equipo_old.ultimo_mantenimiento:
                        equipo_edit.horas_utilizadas= 0
                    equipo_edit.save()
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
            return reverse_lazy('produccion:equipo_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:equipo_list')


class EquipoDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Equipo
    form_class = EquipoForm
    success_url = reverse_lazy('produccion:equipo_list')
    permission_required = 'produccion.delete_equipo'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:equipo_list')


class OrdenCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    template_name = 'orden/orden_add.html'
    success_url = reverse_lazy('produccion:orden_list')
    permission_required = 'produccion.add_ordenelaboracion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                materia = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad = FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad > 0:
                        formula = FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m = f.toJSON()
                            materia.append(m)

                        item['materias'] = materia
                    item['value'] = i.nombre
                    data.append(item)

            elif action == 'search_materias':
                data = []
                mats = MateriaPrima.objects.filter(nombre__icontains=request.POST['term'])
                for i in mats:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    stock=StockMateriaPrima.objects.get(materia_id=i.id)
                    item['cantidad_stock']=stock.cantidad_stock
                    data.append(item)
            elif action == 'search_equipos':
                data = []
                eqs = Equipo.objects.filter(nombre__icontains=request.POST['term'])
                for i in eqs:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'search_formula':
                data =[]
                materia = []
                producto=Producto.objects.get(id=request.POST['term'])
                item=producto.toJSON()
                cantidad = FormulaProducto.objects.filter(producto_id=request.POST['term'],cantidad_teorica=request.POST['cantidad']).count()
                if cantidad > 0:
                    formula = FormulaProducto.objects.filter(producto_id=request.POST['term'],cantidad_teorica=request.POST['cantidad'])
                    for f in formula:
                        m = f.toJSON()
                        materia.append(m)
                    item['materias']=materia
                    data.append(item)

      
                
       
            elif action == 'add':
                print('entro xd')
                orden = json.loads(request.POST['orden'])
                ordenv = OrdenElaboracion()
                ordenv.fecha_emision = datetime.now()

                ordenv.fecha_vigencia = orden['fecha_vigencia']
                print('entro 2')

                print(orden['estado'])
                ordenv.estado = orden['estado']
                ordenv.descripcion_modificacion = orden['descripcion_modificacion']
                ordenv.producto_id = orden['producto']
                ordenv.cantidad_teorica = orden['cantidad_teorica']

                ordenv.aprobado_por = orden['aprobado_por']
                ordenv.verificado_por = orden['verificado_por']
                ordenv.elaborado_por = orden['elaborado_por']

                cantidad = OrdenElaboracion.objects.all().count()

                if cantidad == 0:
                    ordenv.numero = 1
                else:
                    maximo = OrdenElaboracion.objects.aggregate(Max('numero')).get('numero__max')
                    ordenv.numero = maximo + 1

                ordenv.save()
                print('Se guardo la orden')
                for i in orden['materias']:
                    print('entro xs')

                    det = DetalleOrdenElaboracion()
                    det.orden_id = ordenv.id
                    det.materia_id = i['id']
                    det.cantidad = i['cantidad']
                    det.inci = i['inci']
                    det.unidad_medida = i['unidad_medida']
      

                    det.save()
                    print('guardo en detalle')

                for i in orden['equipos']:
                    print(int(i['horas_trabajo']))
                    edet = EquipoOrdenElaboracion()
                    edet.horas_trabajo=int(i['horas_trabajo'])
                    equipo=Equipo.objects.get(id=i['id'])
                    equipo.horas_utilizadas=equipo.horas_utilizadas+ int(i['horas_trabajo'])
                    equipo.save()
                    edet.orden_id = ordenv.id
                    edet.equipo_id = i['id']
                    edet.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class OrdenUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    template_name = 'orden/orden_edit.html'
    success_url = reverse_lazy('produccion:orden_list')
    permission_required = 'produccion.change_ordenelaboracion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                materia = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad = FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad > 0:
                        formula = FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m = f.toJSON()
                            materia.append(m)

                        item['materias'] = materia
                    item['value'] = i.nombre
                    data.append(item)

            elif action == 'search_materias':
                data = []
                mats = MateriaPrima.objects.filter(nombre__icontains=request.POST['term'])
                for i in mats:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'search_equipos':
                data = []
                eqs = Equipo.objects.filter(nombre__icontains=request.POST['term'])
                for i in eqs:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'edit':
                print('entro xd')
                orden = json.loads(request.POST['orden'])
                ordenv = self.get_object()
                estado_anterior = ordenv.estado
                ordenv.fecha_vigencia = orden['fecha_vigencia']
                print('entro 2')
                ordenv.descripcion_modificacion = orden['descripcion_modificacion']
                ordenv.producto_id = orden['producto']
                ordenv.cantidad_teorica = orden['cantidad_teorica']
                ordenv.aprobado_por = orden['aprobado_por']
                ordenv.verificado_por = orden['verificado_por']
                ordenv.elaborado_por = orden['elaborado_por']
                cantidad = OrdenElaboracion.objects.all().count()
                if orden['estado'] == 'FINALIZADA' and ordenv.estado != 'FINALIZADA':
                    print('entro 3')
                    stock = StockProductos.objects.get(producto_id=ordenv.producto_id)
                    print('entro 4')
                    producto = Producto.objects.get(id=ordenv.producto_id)
                    print(ordenv.cantidad_teorica)
                    cantidad_producto = float(ordenv.cantidad_teorica) / ((producto.cantidad_contenido) / float(1000))
                    print(cantidad_producto)
                    stock.cantidad = stock.cantidad + cantidad_producto
                    stock.save()
                ordenv.estado = orden['estado']
                ordenv.save()
                print('Se edito la orden')
                DetalleOrdenElaboracion.objects.filter(orden_id=ordenv.id).delete()
                for i in orden['materias']:
                    det = DetalleOrdenElaboracion()
                    det.orden_id = ordenv.id
                    det.materia_id = i['id']
                    det.cantidad = i['cantidad']
                    print(i['cantidad'])
                    det.inci = i['inci']
                    det.unidad_medida = i['unidad_medida']
                    det.save()
                    print('se guardo el detalle')
                    if ordenv.estado == 'EN PRODUCCION' and estado_anterior != 'EN PRODUCCION':
                        stock = StockMateriaPrima.objects.get(materia_id=det.materia_id)
                        stock.cantidad_stock = stock.cantidad_stock - det.cantidad
                        stock.save()

                    print('edito en detalle')
                EquipoOrdenElaboracion.objects.filter(orden_id=ordenv.id).delete()
                for i in orden['equipos']:
                    edet = EquipoOrdenElaboracion()
                    print(i['horas_utiles'])
                    edet.horas_trabajo=int(i['horas_trabajo'])
                    edet.orden_id = ordenv.id
                    edet.equipo_id = i['id']
                    edet.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_materias(self):
        data = []
        try:
            for i in DetalleOrdenElaboracion.objects.filter(orden_id=self.get_object().id):
                item = i.materia.toJSON()
                item['cantidad'] = i.cantidad
                item['producto_id'] = self.get_object().producto.id
                item['producto'] = self.get_object().producto.nombre
                data.append(item)
        except:
            pass
        return data

    def get_details_equipos(self):
        data = []
        try:
            for i in EquipoOrdenElaboracion.objects.filter(orden_id=self.get_object().id):
                item = i.equipo.toJSON()
                item['horas_trabajo']=i.horas_trabajo
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Orden'
        context['entity'] = 'Produccion'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_materias())
        context['equi'] = json.dumps(self.get_details_equipos())

        return context


class OrdenListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = OrdenElaboracion
    template_name = 'orden/orden_list.html'
    permission_required = 'produccion.view_ordenelaboracion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in OrdenElaboracion.objects.all():
                    data.append(i.toJSON())

                response = JsonResponse(data, safe=False)
                response.status_code = 201
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ordenes de Elaboracion'
        context['create_url'] = reverse_lazy('produccion:orden_add')
        context['list_url'] = reverse_lazy('produccion:orden_list')
        return context


class OrdenDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    success_url = reverse_lazy('produccion:orden_list')
    permission_required = 'produccion.delete_ordenelaboracion'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:orden_list')


class FormulaCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Formula
    form_class = FormulaForm
    template_name = 'formulas/formulas_add.html'
    success_url = reverse_lazy('produccion:orden_list')
    permission_required = 'produccion.add_formula'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_materias':
                data = []
                mats = MateriaPrima.objects.filter(nombre__icontains=request.POST['term'])
                for i in mats:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'search_products':
                data = []
                materia = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad = FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad > 0:
                        formula = FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m = f.toJSON()
                            materia.append(m)

                        item['materias'] = materia
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'search_formula':
                data =[]
                materia = []
                producto=Producto.objects.get(id=request.POST['term'])
                item=producto.toJSON()
                cantidad = FormulaProducto.objects.filter(producto_id=request.POST['term'],cantidad_teorica=request.POST['cantidad']).count()
                if cantidad > 0:
                    formula = FormulaProducto.objects.filter(producto_id=request.POST['term'],cantidad_teorica=request.POST['cantidad'])
                    for f in formula:
                        m = f.toJSON()
                        materia.append(m)
                    item['materias']=materia
                    data.append(item)

      
                
            elif action == 'add':
                print('entro xd')
                orden = json.loads(request.POST['orden'])
                formula= Formula()
                formula.producto_id=orden['producto']
                formula.cantidad_teorica=orden['cantidad_teorica']
                formula.save()
                for i in orden['materias']:
                    print('entro xs')
                    formulav = FormulaProducto()
                    formulav.formula_id=formula.id
                    formulav.producto_id = orden['producto']
                    formulav.cantidad_teorica = orden['cantidad_teorica']
                    formulav.materia_id = i['id']
                    formulav.cantidad = i['cantidad']
                    formulav.save()
                    print('guardo la formula')

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

class FormulaUpdateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Formula
    form_class = FormulaForm
    template_name = 'formulas/formulas_edit.html'
    success_url = reverse_lazy('produccion:orden_list')
    permission_required = 'produccion.change_formula'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_materias':
                data = []
                mats = MateriaPrima.objects.filter(nombre__icontains=request.POST['term'])
                for i in mats:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'search_products':
                data = []
                materia = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad = FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad > 0:
                        formula = FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m = f.toJSON()
                            materia.append(m)

                        item['materias'] = materia
                    item['value'] = i.nombre
                    data.append(item)
   
            elif action == 'edit':
                print('entro xd')
                orden = json.loads(request.POST['orden'])
                formula=self.get_object()
                formula.producto_id=orden['producto']
                formula.cantidad_teorica=orden['cantidad_teorica']
                formula.save()
                FormulaProducto.objects.filter(formula_id=formula.id).delete()
                for i in orden['materias']:
                    formulav = FormulaProducto()
                    formulav.formula_id=formula.id
                    formulav.producto_id = orden['producto']
                    formulav.cantidad_teorica = orden['cantidad_teorica']
                    formulav.materia_id = i['id']
                    formulav.cantidad = i['cantidad']
                    formulav.save()
                    print('edito la formula la formula')

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_materias(self):
        data = []
        try:
            for i in FormulaProducto.objects.filter(formula_id=self.get_object().id):
                item = i.materia.toJSON()
                item['cantidad'] = i.cantidad
                item['producto_id'] = self.get_object().producto.id
                item['unidad_medida_producto'] = self.get_object().producto.unidad_medida
                item['producto'] = self.get_object().producto.nombre
                item['cantidad_teorica']=self.get_object().cantidad_teorica
                data.append(item)
        except:
            pass
        return data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Formula'
        context['entity'] = 'Produccion'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_materias())

        return context

class FormulaListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Formula
    template_name = 'formulas/formulas_list.html'
    permission_required = 'produccion.view_formula'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Formula.objects.all():
                    data.append(i.toJSON())
                print (data)

                response = JsonResponse(data, safe=False)
                response.status_code = 201
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Formulas'
        context['create_url'] = reverse_lazy('produccion:formula_add')
        context['list_url'] = reverse_lazy('produccion:formula_list')
        return context

class FormulaDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Formula
    form_class = FormulaForm
    success_url = reverse_lazy('produccion:formula_list')
    permission_required = 'produccion.delete_formula'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:orden_list')
