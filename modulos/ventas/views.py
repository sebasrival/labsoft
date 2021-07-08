from django.shortcuts import render
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,View
from .models import Cliente, DatosFacturacion,FacturaVenta,FacturaVentaDetalle,Cobro,Cuota, Pedido,PedidoDetalle,PuntoVenta
from modulos.produccion.models import Producto, StockProductos
from .forms import ClienteForm,FacturaVentaForm,PedidoForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from xhtml2pdf import pisa
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template
import json

# Vistas de clientes
from ..accounts.mixins import PermissionMixin


class ClienteCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/clientes_add.html'
    success_url = reverse_lazy('ventas:cliente_list')
    permission_required = 'ventas.add_cliente'

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
            return redirect('ventas:cliente_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('ventas:cliente_list')


class ClienteListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Cliente
    template_name = 'clientes/clientes_list.html'
    permission_required = 'ventas.view_cliente'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for client in self.get_queryset():
                    cliente = {
                        'ruc': client.ruc,
                        'razon_social': client.razon_social,
                        'cedula': client.cedula,
                        'telefono': client.telefono,
                        'email': client.email,
                        'direccion': client.direccion,
                        'nombre': client.nombre,
                        'apellido': client.apellido,
                        'id': client.id
                    }
                    data.append(cliente)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'clientes',
                'subtitle': 'Lista de clientes',
                'route': reverse_lazy('ventas:cliente_list'),
                'form': ClienteForm()
            }
            return render(request, self.template_name, context)


class ClienteUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/clientes_edit.html'
    success_url = reverse_lazy('ventas:cliente_list')
    permission_required = 'ventas.change_cliente'

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
            return reverse_lazy('ventas:cliente_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('ventas:cliente_list')


class ClienteDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy('ventas:cliente_list')
    permission_required = 'ventas.delete_cliente'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('ventas:cliente_list')


#Vistas para Facturas Venta
class FacturaVentaCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = FacturaVenta
    form_class = FacturaVentaForm
    template_name = 'facturas/facturas_add.html'
    success_url = reverse_lazy('ventas:factura_list')
    # url_redirect = success_url
    permission_required = 'ventas.add_facturaventa'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    stock=StockProductos.objects.get(producto_id=i.id)
                    item['value'] = i.nombre
                    item['cantidad_stock']=stock.cantidad
                    data.append(item)
            elif action == 'set_punto_venta':
                data = []
              
                punto = PuntoVenta.objects.get(numero=int(request.POST['term']))
                numero=DatosFacturacion.objects.get(punto_venta=punto.codigo)
                item=numero.toJSON()
                data.append(item)
            elif action == 'search_clientes':
                data = []
                clients = Cliente.objects.filter(ruc__icontains=request.POST['term'])
                for i in clients:
                    item = i.toJSON()
                    item['value'] = i.ruc
                    data.append(item)
            elif action == 'add':
                factura= json.loads(request.POST['factura'])
                facturav = FacturaVenta()
                facturav.nro_factura=factura['nro_factura']
                facturav.fecha_emision = factura['fecha_emision']
                datos=DatosFacturacion.objects.get(sucursal=factura['sucursal'],punto_venta=factura['punto_venta'])
                datos.numeracion_actual=int(factura['numeracion_actual'])+1
                datos.save()
                punto_venta=PuntoVenta.objects.get(codigo=factura['punto_venta'])
                facturav.punto_venta_id=punto_venta.id
                print (factura['cliente_ruc'])
                if (factura['cliente_ruc']==''):
                    facturav.cliente_id = factura['cliente']
                else:
                    c=Cliente()
                    c.ruc=factura['cliente_ruc']
                    c.razon_social=factura['cliente_razon_social']
                    c.cedula=factura['cliente_ruc']
                    c.save()
                    print('Se agrego el cliente')
                    facturav.cliente_id =c.id
                facturav.monto_iva1 = float(factura['total_iva10'])
                facturav.monto_iva2 = float(factura['total_iva5'])
                facturav.total = float(factura['total_factura'])
                facturav.tipo_venta= factura['tipo_cobro']
                if factura['tipo_cobro']=='Contado' :   
                    facturav.estado='PAGADA'
                else:
                    facturav.estado='PENDIENTE'

                facturav.exenta=0
                cobro=Cobro()
                cobro.cantidad_cuotas=factura['cant_cuotas']
                cobro.metodo_cobro=factura['tipo_cobro']
                cobro.medio_cobro=factura['metodo_cobro']
                cobro.save()
                fecha=datetime.now()
                i=0
                while i < int(factura['cant_cuotas']):
                    cuota=Cuota()
                    cuota.estado='PENDIENTE'
                    cuota.nro_cuota=(i+1)
                    cuota.monto_cuota=round(facturav.total/int(cobro.cantidad_cuotas))
                    fecha=fecha+ timedelta(days=30)
                    cuota.fecha_vencimiento=fecha 
                    cuota.cobro_id=cobro.id

                    cuota.save()
                    print(cuota.cobro_id)

                    i=i+1
                facturav.cobro_id=cobro.id
                facturav.save()
                for i in factura['productos']:
                    det = FacturaVentaDetalle()
                    det.factura_id = facturav.id
                    det.producto_id= i['id']
                    det.cantidad = int(i['cantidad'])
                    det.precio = float(i['precio'])
                    det.save()
                    stock=StockProductos.objects.get(producto_id=i['id'])
                    stock.cantidad=stock.cantidad- int(i['cantidad'])
                    stock.save()
            
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_details_product(self,id):
        data = []
        try:
            for i in PedidoDetalle.objects.filter(pedido_id=id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                stock=StockProductos.objects.get(producto_id=i.producto.id)
                item['cantidad_stock']=stock.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_details_pedido(self,pedido_id):
        data = []
        try:
            pedido=Pedido.objects.get(id=pedido_id)
            item = pedido.toJSON()
            item['fecha_pedido']=None
            item['fecha_entrega']=None

            data.append(item)
        except:
            pass
        return data
    def get_punto_venta(self):
        data = []
        try:
            punto=PuntoVenta.objects.all()
            for i in punto:
                item = i.toJSON()
                print(item['numero'])
                data.append(item)
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_pedido= self.kwargs.get('pedidoid')
        context['puntos'] = self.get_punto_venta()

        if (id_pedido!=''):
            context['det'] = json.dumps(self.get_details_product(id_pedido))
            context['pedidodet'] = json.dumps(self.get_details_pedido(id_pedido))

        return context
        

class FacturaVentaListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = FacturaVenta
    template_name = 'facturas/facturas_list.html'
    permission_required = 'ventas.view_facturaventa'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in FacturaVenta.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_cobro':
                data = []
                fv=FacturaVenta.objects.get(id=request.POST['id'])
                cobro=fv.cobro_id
                print(cobro)
                for i in Cuota.objects.filter(cobro_id=cobro):
                    data.append(i.toJSON())
            elif action == 'anular_factura':
                data = []
                fv=FacturaVenta.objects.get(id=request.POST['id'])
                fv.estado='ANULADA'
                fv.save()
            elif action=='edit_cuota':
                cuota=Cuota.objects.get(id=request.POST['cuota_id'])
                cuota.estado=request.POST['estado']
                if request.POST['estado']=='PAGADA':
                    cuota.fecha_pago_cuota=datetime.now()
                else:
                    cuota.fecha_pago_cuota=None
                cuota.save()
                fv=FacturaVenta.objects.get(cobro_id=cuota.cobro_id)
                pendientes= Cuota.objects.filter(estado='PENDIENTE',cobro_id=cuota.cobro_id).count()
                if pendientes ==0 :
                    fv.estado='PAGADA'
                    fv.save()
                else:
                    fv.estado='PENDIENTE'
                    fv.save()

                
                data['message'] = f'¡{self.model.__name__} registrado correctamente!'
                data['error'] = '¡Sin errores!'
                response = JsonResponse(data, safe=False)
                response.status_code = 201
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de facturas'
        context['create_url'] = reverse_lazy('ventas:factura_add')
        context['list_url'] = reverse_lazy('ventas:factura_list')
        return context


class FacturaVentaUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = FacturaVenta
    form_class = FacturaVentaForm
    template_name = 'facturas/facturas_edit.html'
    success_url = reverse_lazy('ventas:factura_list')
    # url_redirect = success_url
    permission_required = 'ventas.change_facturaventa'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    stock=StockProductos.objects.get(producto_id=i.id)
                    item['value'] = i.nombre
                    item['cantidad_stock']=stock.cantidad
                    data.append(item)
            elif action == 'search_clientes':
                data = []
                clients = Cliente.objects.filter(ruc__icontains=request.POST['term'])
                for i in clients:
                    item = i.toJSON()
                    item['value'] = i.ruc
                    data.append(item)
            elif action == 'edit':
                factura= json.loads(request.POST['factura'])
                facturav = self.get_object()
                facturav.nro_factura=factura['nro_factura']
                facturav.fecha_emision = factura['fecha_emision']
                if (factura['cliente_ruc']==''):
                    facturav.cliente_id = factura['cliente']
                else:
                    c=Cliente()
                    c.ruc=factura['cliente_ruc']
                    c.razon_social=factura['cliente_razon_social']
                    c.cedula=factura['cliente_ruc']
                    c.save()
                    print('Se agrego el cliente')
                    facturav.cliente_id =c.id

                facturav.monto_iva1 = float(factura['total_iva10'])
                facturav.monto_iva2 = float(factura['total_iva5'])
                facturav.exenta=float(factura['total_exenta'])
                facturav.total = float(factura['total_factura'])
                if int(factura['cobro_edit'])==1: 
                    Cuota.objects.filter(cobro_id=facturav.cobro_id).delete()
                    facturav.tipo_venta= factura['tipo_cobro']
                
                    if factura['tipo_cobro']=='Contado' :   
                        facturav.estado='PAGADA'
                    else:
                        facturav.estado='PENDIENTE'
                    cobro=Cobro()
                    cobro.cantidad_cuotas=factura['cant_cuotas']
                    cobro.metodo_cobro=factura['tipo_cobro']
                    cobro.medio_cobro=factura['metodo_cobro']
                    print(factura['metodo_cobro'])
                
                    cobro.save()
                    fecha=datetime.now()
                    i=0
                    while i < int(factura['cant_cuotas']):
                        cuota=Cuota()
                        cuota.estado='PENDIENTE'
                        cuota.nro_cuota=(i+1)
                        cuota.monto_cuota=round(facturav.total/int(cobro.cantidad_cuotas))
                        fecha=fecha+ timedelta(days=30)
                        cuota.fecha_vencimiento=fecha 
                        cuota.cobro_id=cobro.id
                        cuota.save()
                        print(cuota.cobro_id)
                        i=i+1
                
                    cobro_anterior=facturav.cobro_id
                    facturav.cobro_id=cobro.id
                    facturav.save()
                    Cobro.objects.filter(id=cobro_anterior).delete()
                facturav.save()
                detalles=FacturaVentaDetalle.objects.filter(factura_id=facturav.id)
                for i in detalles:
                    stock=StockProductos.objects.get(producto_id=i.producto_id)
                    stock.cantidad=stock.cantidad + int(i.cantidad)
                    stock.save()
                
                FacturaVentaDetalle.objects.filter(factura_id=facturav.id).delete()
                for i in factura['productos']:
                    det = FacturaVentaDetalle()
                    det.factura_id = facturav.id
                    det.producto_id= i['id']
                    det.cantidad = int(i['cantidad'])
                    det.precio = float(i['precio'])
                    det.save()
                    stock=StockProductos.objects.get(producto_id=i['id'])
                    stock.cantidad=stock.cantidad- int(i['cantidad'])
                    stock.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in FacturaVentaDetalle.objects.filter(factura_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                stock=StockProductos.objects.get(producto_id=i.producto.id)
                item['cantidad_stock']=stock.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_details_cobro(self):
        data = []
        try:
            cobro=self.get_object().cobro
            cliente=self.get_object().cliente
            item=cobro.toJSON()
            item['monto']=self.get_object().total
            item['fecha']=self.get_object().fecha_emision.strftime('%m/%d/%Y')
            item['estado']=self.get_object().estado
            item['razon_social']=cliente.razon_social
            item['cliente_id']=cliente.id
            item['ruc']=cliente.ruc
            data.append(item)
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Factura'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        context['cobro']=json.dumps(self.get_details_cobro())
        return context


class FacturaVentaDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = FacturaVenta
    form_class = FacturaVentaForm
    success_url = reverse_lazy('ventas:factura_list')
    permission_required = 'ventas.delete_facturaventa'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('ventas:factura_list')


class FacturaPdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('facturas/factura_invoice.html')
            factura= FacturaVenta.objects.get(pk=self.kwargs['pk'])
            punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)

            context = {
                'factura': FacturaVenta.objects.get(pk=self.kwargs['pk']),
                'datos_facturacion': DatosFacturacion.objects.get(punto_venta=punto_venta.codigo),
                'comp': {'name': 'LABORATORIO OCAMPOS SRL', 'ruc': '9999999999999', 'address': 'San Lorenzo, Paraguay'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('ventas:factura_list'))


class PedidoCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedidos_add.html'
    success_url = reverse_lazy('ventas:pedido_list')
    # url_redirect = success_url
    permission_required = 'ventas.add_pedido'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    stock=StockProductos.objects.get(producto_id=i.id)
                    item['value'] = i.nombre
                    item['cantidad_stock']=stock.cantidad
                    data.append(item)
    
            elif action == 'search_clientes':
                data = []
                clients = Cliente.objects.filter(ruc__icontains=request.POST['term'])
                for i in clients:
                    item = i.toJSON()
                    item['value'] = i.ruc
                    data.append(item)
            elif action == 'add':
                pedido= json.loads(request.POST['factura'])
                pedidov = Pedido()
                pedidov.fecha_pedido = datetime.now()
                pedidov.fecha_entrega=None
                pedidov.estado=pedido['estado_pedido']
                if (pedido['cliente_ruc']==''):
                    pedidov.cliente_id = pedido['cliente']
                else:
                    c=Cliente()
                    c.ruc=pedido['cliente_ruc']
                    c.razon_social=pedido['cliente_razon_social']
                    c.cedula=pedido['cliente_ruc']
                    c.save()
                    print('Se agrego el cliente')
                    pedidov.cliente_id =c.id
                pedidov.total=int(pedido['total_factura'])
                print(pedidov.total)
                print(pedidov.fecha_pedido)
                print(pedidov.fecha_entrega)
                print(pedidov.estado)
                print(pedidov.cliente_id)
                pedidov.save()
                for i in pedido['productos']:
                    det = PedidoDetalle()
                    det.pedido_id = pedidov.id
                    det.producto_id= i['id']
                    det.cantidad = int(i['cantidad'])
                    det.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)    


class PedidoUpdateView(LoginRequiredMixin, PermissionMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedidos_edit.html'
    success_url = reverse_lazy('ventas:pedido_list')
    #url_redirect = success_url
    permission_required = 'ventas.change_pedido'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'])
                for i in prods:
                    item = i.toJSON()
                    stock=StockProductos.objects.get(producto_id=i.id)
                    item['value'] = i.nombre
                    item['cantidad_stock']=stock.cantidad
                    data.append(item)
    
            elif action == 'search_clientes':
                data = []
                clients = Cliente.objects.filter(ruc__icontains=request.POST['term'])
                for i in clients:
                    item = i.toJSON()
                    item['value'] = i.ruc
                    data.append(item)
            elif action == 'edit':
                print('entro')
                pedido= json.loads(request.POST['factura'])
                pedidov = Pedido.objects.get(id=self.get_object().id)
                print(pedido['estado_pedido'])

                if (pedido['estado_pedido']=='FINALIZADO'):      
                    pedidov.fecha_entrega=datetime.now()
            
                pedidov.estado=pedido['estado_pedido']
                if (pedido['cliente_ruc']==''):
                    pedidov.cliente_id = pedido['cliente']
                else:
                    c=Cliente()
                    c.ruc=pedido['cliente_ruc']
                    c.razon_social=pedido['cliente_razon_social']
                    c.cedula=pedido['cliente_ruc']
                    c.save()
                    print('Se agrego el cliente')
                    pedidov.cliente_id =c.id
                pedidov.total=int(pedido['total_factura'])
                print('entro')

                pedidov.save()
                PedidoDetalle.objects.filter(pedido_id=pedidov.id).delete()
                for i in pedido['productos']:
                    det = PedidoDetalle()
                    det.pedido_id = pedidov.id
                    det.producto_id= i['id']
                    det.cantidad = int(i['cantidad'])
                    det.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)    
    def get_details_product(self):
        data = []
        try:
            for i in PedidoDetalle.objects.filter(pedido_id=self.get_object().id):
                item = i.producto.toJSON()
                item['cantidad'] = i.cantidad
                stock=StockProductos.objects.get(producto_id=i.producto.id)
                item['cantidad_stock']=stock.cantidad
                data.append(item)
        except:
            pass
        return data

    def get_details_pedido(self):
        data = []
        try:
            pedido=Pedido.objects.get(id=self.get_object().id)
            item = pedido.toJSON()
            item['fecha_pedido']=None
            item['fecha_entrega']=None

            data.append(item)
        except:
            pass
        return data
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_pedido= self.kwargs.get('pedidoid')
        if (id_pedido!=''):
            context['det'] = json.dumps(self.get_details_product())
            context['pedidodet'] = json.dumps(self.get_details_pedido())

        return context


class PedidoListView(LoginRequiredMixin, PermissionMixin, ListView):
    model = Pedido
    template_name = 'pedidos/pedidos_list.html'
    permission_required = 'ventas.view_pedido'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pedido.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_pedido':
                data = []
                print(request.POST['id'])
                for i in PedidoDetalle.objects.filter(pedido_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        context['create_url'] = reverse_lazy('ventas:pedido_add')
        context['list_url'] = reverse_lazy('ventas:pedido_list')
        return context


class PedidoDeleteView(LoginRequiredMixin, PermissionMixin, DeleteView):
    model = Pedido
    form_class = PedidoForm
    success_url = reverse_lazy('ventas:factura_list')
    permission_required = 'ventas.delete_pedido'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('ventas:pedido_list')