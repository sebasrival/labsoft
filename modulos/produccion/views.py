from modulos.compras.models import StockMateriaPrima
from django.shortcuts import render
from django.db.models import Max

# Create your views here.
from django.shortcuts import render
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
# Vistas de productos
class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_add.html'
    success_url = reverse_lazy('produccion:producto_list')


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
                    p=Producto.objects.get(codigo_producto=form['codigo_producto'].value())
                    s=StockProductos(cantidad=0,producto_id=p.id)
                    s.save()

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

 
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/productos_list.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prod in self.get_queryset():
                    stock=StockProductos.objects.get(producto_id=prod.id)
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


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_edit.html'
    success_url = reverse_lazy('produccion:producto_list')

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


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('produccion:producto_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:producto_list')

# Seccion de equipos.



class EquipoCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    form_class = EquipoForm
    template_name = 'equipos/equipos_add.html'
    success_url = reverse_lazy('produccion:equipo_list')


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

 
class EquipoListView(LoginRequiredMixin, ListView):
    model = Equipo
    template_name = 'equipos/equipos_list.html'

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


class EquipoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipo
    form_class = EquipoForm
    template_name = 'equipos/equipos_edit.html'
    success_url = reverse_lazy('produccion:equipo_list')

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
            return reverse_lazy('produccion:equipo_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:equipo_list')


class EquipoDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipo
    form_class = EquipoForm
    success_url = reverse_lazy('produccion:equipo_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:equipo_list')




class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    template_name = 'orden/orden_add.html'
    success_url = reverse_lazy('ventas:orden_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                materia=[]
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad=FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad> 0:
                        formula=FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m=f.toJSON()
                            materia.append(m)
                        
                        item['materias']=materia
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
            elif action == 'add':
                print ('entro xd')
                orden= json.loads(request.POST['orden'])
                ordenv = OrdenElaboracion()
                ordenv.fecha_emision= datetime.now()

                ordenv.fecha_vigencia=orden['fecha_vigencia']
                print ('entro 2')

                print(orden['estado'])
                ordenv.estado=orden['estado']
                ordenv.descripcion_modificacion=orden['descripcion_modificacion']
                ordenv.producto_id=orden['producto']
                ordenv.cantidad_teorica=orden['cantidad_teorica']
     

                ordenv.aprobado_por=orden['aprobado_por']
                ordenv.verificado_por=orden['verificado_por']
                ordenv.elaborado_por=orden['elaborado_por']

                cantidad=OrdenElaboracion.objects.all().count()

                if cantidad==0:
                    ordenv.numero=1
                else:
                    maximo=OrdenElaboracion.objects.aggregate(Max('numero')).get('numero__max') 
                    ordenv.numero=maximo+1
                

                ordenv.save()
                print('Se guardo la orden')
                for i in orden['materias']:
                    print('entro xs')

                    det = DetalleOrdenElaboracion()
                    det.orden_id = ordenv.id
                    det.materia_id= i['id']
                    det.cantidad = i['cantidad']
                    det.inci= i['inci']
                    det.unidad_medida= i['unidad_medida']
                    print(det.orden_id)
                    print(det.materia_id)
                    print(det.cantidad)
                    print(det.inci)
                    print(det.unidad_medida)
                    print('entro x2')

                    det.save()
                    print('guardo en detalle')

                for i in orden['equipos']:
                    edet = EquipoOrdenElaboracion()
                    edet.orden_id = ordenv.id
                    edet.equipo_id= i['id']
                    edet.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)   



class OrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    template_name = 'orden/orden_edit.html'
    success_url = reverse_lazy('ventas:orden_list')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                materia=[]
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    cantidad=FormulaProducto.objects.filter(producto_id=i.id).count()
                    if cantidad> 0:
                        formula=FormulaProducto.objects.filter(producto_id=i.id)
                        for f in formula:
                            m=f.toJSON()
                            materia.append(m)
                        
                        item['materias']=materia
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
                print ('entro xd')
                orden= json.loads(request.POST['orden'])
                ordenv = self.get_object()
                estado_anterior=ordenv.estado
                ordenv.fecha_vigencia=orden['fecha_vigencia']
                print ('entro 2')
                ordenv.descripcion_modificacion=orden['descripcion_modificacion']
                ordenv.producto_id=orden['producto']
                ordenv.cantidad_teorica=orden['cantidad_teorica']
                ordenv.aprobado_por=orden['aprobado_por']
                ordenv.verificado_por=orden['verificado_por']
                ordenv.elaborado_por=orden['elaborado_por']
                cantidad=OrdenElaboracion.objects.all().count()
                if orden['estado']=='FINALIZADA' and ordenv.estado!='FINALIZADA':
                    print('entro 3')
                    stock=StockProductos.objects.get(producto_id=ordenv.producto_id)
                    print('entro 4')
                    producto=Producto.objects.get(id=ordenv.producto_id)
                    print(ordenv.cantidad_teorica)
                    cantidad_producto=float(ordenv.cantidad_teorica)/((producto.cantidad_contenido)/float(1000))
                    print (cantidad_producto)
                    stock.cantidad=stock.cantidad+cantidad_producto
                    stock.save()
                ordenv.estado=orden['estado']
                ordenv.save()
                print('Se edito la orden')
                DetalleOrdenElaboracion.objects.filter(orden_id=ordenv.id).delete()
                for i in orden['materias']:
                    det = DetalleOrdenElaboracion()
                    det.orden_id = ordenv.id
                    det.materia_id= i['id']
                    det.cantidad = i['cantidad']
                    print(i['cantidad'])
                    det.inci= i['inci']
                    det.unidad_medida= i['unidad_medida']
                    det.save()
                    print('se guardo el detalle')
                    if ordenv.estado== 'EN PRODUCCION' and estado_anterior !='EN PRODUCCION':
                        stock=StockMateriaPrima.objects.get(materia_id=det.materia_id)
                        stock.cantidad=stock.cantidad-det.cantidad
                        stock.save()
           
                    print('edito en detalle')
                EquipoOrdenElaboracion.objects.filter(orden_id=ordenv.id).delete()
                for i in orden['equipos']:
                    edet = EquipoOrdenElaboracion()
                    edet.orden_id = ordenv.id
                    edet.equipo_id= i['id']
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
                item['producto_id']=self.get_object().producto.id
                item['producto']=self.get_object().producto.nombre
                data.append(item)
        except:
            pass
        return data

    def get_details_equipos(self):
        data = []
        try:
            for i in EquipoOrdenElaboracion.objects.filter(orden_id=self.get_object().id):
                item = i.equipo.toJSON()
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


class OrdenListView(LoginRequiredMixin, ListView):
    model = OrdenElaboracion
    template_name = 'orden/orden_list.html'

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

class OrdenDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenElaboracion
    form_class = OrdenElaboracionForm
    success_url = reverse_lazy('produccion:orden_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:orden_list')