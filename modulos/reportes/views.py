from modulos.ventas.views import FacturaVentaDeleteView
from django.shortcuts import render
from django.shortcuts import render
import os
import locale
import numpy as np

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import View
from xhtml2pdf import pisa
from modulos.produccion.models import Equipo, OrdenElaboracion
from modulos.ventas.models import *

from modulos.accounts.models import User
from datetime import datetime
from datetime import date

from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import get_template

# Create your views here.




def PantallaReporteVenta(request):
 
    return render(request, "ventas/venta_filtro.html")

def PantallaReporteOrden(request):
 
    return render(request, "produccion/generar_reporte_orden.html")

def PantallaReporteVentaMensual(request):

    MESES = [
    ('Enero', 1),
    ('Febrero',2),
    ('Marzo', 3),
    ('Abril', 4),
    ('Mayo', 5),
    ('Junio', 6),
    ('Julio', 7),
    ('Agosto', 8),
    ('Setiembre', 9),
    ('Octubre', 10),
    ('Noviembre', 11),
    ('Diciembre', 12)
    ]
    context = {
                'meses': MESES,
             
            }
    return render(request, "ventas/generar_reporte_mensual.html",context)
def PantallaReporteProductoMensual(request):

    MESES = [
    ('Enero', 1),
    ('Febrero',2),
    ('Marzo', 3),
    ('Abril', 4),
    ('Mayo', 5),
    ('Junio', 6),
    ('Julio', 7),
    ('Agosto', 8),
    ('Setiembre', 9),
    ('Octubre', 10),
    ('Noviembre', 11),
    ('Diciembre', 12)
    ]
    context = {
                'meses': MESES,
             
            }
    return render(request, "produccion/generar_productos_mensual.html",context)
class MantenimientoEquipoPdfView(View):

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
            template = get_template('produccion/reporte_mantenimiento.html')
            #punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario=User.objects.get(id=request.user.id)
            print(usuario)
            now = datetime.now()
            print("La hora actual es {}".format(now.hour))

            context = {
                #'datos_facturacion': DatosFacturacion.objects.get(punto_venta=punto_venta.codigo),
                'equipos': Equipo.objects.all(),
                'usuario': usuario.username,
                'fecha': date.today(),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,
           
                 
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

class ReporteVentaPdfView(View):
    template_name = 'ventas/venta_filtro.html'

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
            template = get_template('ventas/reporte_ventas.html')
            #punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            facturas=FacturaVenta.objects.all()
            usuario=User.objects.get(id=request.user.id)
            now = datetime.now()
            factura=FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).count()
            print(factura)
            if factura == 0 :
                
                total_facturas=0
                total_exentas=0
                total_montoiva1=0
                total_montoiva2=0
                total_gravadas10=0 
                total_gravadas5=0
                total_sin_iva=0
            else: 
                total_facturas=round(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('total')).get('total__sum'))
                total_exentas=round(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('exenta')).get('exenta__sum'))
                total_montoiva1=round(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('monto_iva1')).get('monto_iva1__sum'))
                total_montoiva2=round(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('monto_iva2')).get('monto_iva2__sum'))
                total_gravadas10=round(float(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('monto_iva1')).get('monto_iva1__sum'))* 11) 
                total_gravadas5=round(FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')).aggregate(Sum('monto_iva2')).get('monto_iva2__sum') * 21)
                total_sin_iva=(total_gravadas10-total_montoiva1)+ (total_gravadas5-total_montoiva2)
            context = {
                'facturas': FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year')),
                'usuario': usuario.username,
                'total_ventas':f'{total_facturas:,.0f}',
                'total_exentas':f'{total_exentas:,.0f}',
                'total_montoiva1':f'{total_montoiva1:,.0f}',
                'total_montoiva2':f'{total_montoiva2:,.0f}',
                'total_gravadas10':f'{total_gravadas10:,.0f}',
                'total_gravadas5':f'{total_gravadas5:,.0f}',
                'total_sin_iva':f'{total_sin_iva:,.0f}',
                'anho': self.kwargs.get('year'),

                'fecha': date.today().strftime("%d/%m/%Y"),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,

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
        except Exception as e:
                print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('ventas:factura_list'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ReporteVentaMensualPdfView(View):

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
        MESES = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    


        try:
            template = get_template('ventas/reporte_venta_mensual.html')
            #punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            facturas=FacturaVenta.objects.all()
            usuario=User.objects.get(id=request.user.id)
            now = datetime.now()
            factura=FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes')).count()
            print(factura)
            if factura == 0 :
                
                total_facturas=0
                total_exentas=0
                total_montoiva1=0
                total_montoiva2=0
                total_gravadas10=0 
                total_gravadas5=0
                total_sin_iva=0
            else: 
                total_facturas=round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('total')).get('total__sum'))
                total_exentas=round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('exenta')).get('exenta__sum'))
                total_montoiva1=round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('monto_iva1')).get('monto_iva1__sum'))
                total_montoiva2=round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('monto_iva2')).get('monto_iva2__sum'))
                total_gravadas10=round(float(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('monto_iva1')).get('monto_iva1__sum'))* 11) 
                total_gravadas5=round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes'),estado='PAGADA').aggregate(Sum('monto_iva2')).get('monto_iva2__sum') * 21)
                total_sin_iva=(total_gravadas10-total_montoiva1)+ (total_gravadas5-total_montoiva2)
            context = {
                'facturas': FacturaVenta.objects.filter(estado='PAGADA',fecha_emision__year=self.kwargs.get('year'),fecha_emision__month=self.kwargs.get('mes')),
                'usuario': usuario.username,
                'total_ventas':f'{total_facturas:,.0f}',
                'total_exentas':f'{total_exentas:,.0f}',
                'total_montoiva1':f'{total_montoiva1:,.0f}',
                'total_montoiva2':f'{total_montoiva2:,.0f}',
                'total_gravadas10':f'{total_gravadas10:,.0f}',
                'total_gravadas5':f'{total_gravadas5:,.0f}',
                'total_sin_iva':f'{total_sin_iva:,.0f}',
                'mes': MESES[self.kwargs.get('mes')-1],
                'anho': self.kwargs.get('year'),
                'usuario': usuario.username,

                'fecha': date.today().strftime("%d/%m/%Y"),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,

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
        except Exception as e:
                print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('ventas:factura_list'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class ProductoReporte(): 
    codigo = "" 
    nombre = "" 
    cantidad_producida = 0
    cantidad_vendida= 0


class ReporteProductosMensualPdfView(View):

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
        PRODUCTOS = []
        MESES = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
        try:
            template = get_template('produccion/reporte_productos_mensual.html')
            #punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario=User.objects.get(id=request.user.id)
            now = datetime.now()

            vendida_total=0
            producida_total=0
            for producto in Producto.objects.all():
                p=ProductoReporte()
                p.codigo=producto.codigo_producto
                p.nombre=producto.nombre
                p.cantidad_producida=producto.obtener_cantidad_producida(self.kwargs.get('mes'),self.kwargs.get('year'))
                producida_total=producida_total+p.cantidad_producida
                p.cantidad_vendida=producto.obtener_cantidad_vendida(self.kwargs.get('mes'),self.kwargs.get('year'))
                vendida_total=vendida_total +p.cantidad_vendida

                PRODUCTOS.append(p)
                
            print(vendida_total)
            PRODUCTOS.sort(key=lambda x: x.cantidad_vendida, reverse=True)
            if (PRODUCTOS[0].cantidad_vendida == 0):
                mas_vendida= 'NINGUNO'
            else:
                mas_vendida=PRODUCTOS[0].nombre

            PRODUCTOS.sort(key=lambda x: x.cantidad_producida, reverse=True)
            if (PRODUCTOS[0].cantidad_producida == 0):
                mas_producida= 'NINGUNO'
            else:
                mas_producida=PRODUCTOS[0].nombre
            context = {
                'productos': Producto.objects.all(),
                'lista_producto': PRODUCTOS,
                'usuario': usuario.username,
                #'total_ventas':f'{total_facturas:,.0f}',
                'mes': MESES[self.kwargs.get('mes')-1],
                'anho': self.kwargs.get('year'),
                'usuario': usuario.username,
                'producida_total': int(producida_total),
                'vendida_total': vendida_total,
                'usuario': usuario.username,
                'mas_vendida':mas_vendida,
                'mas_producida':mas_producida,

                'fecha': date.today().strftime("%d/%m/%Y"),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,

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
        except Exception as e:
                print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('ventas:factura_list'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class ReporteOrdenPdfView(View):

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
        MESES = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    


        try:
            template = get_template('produccion/reporte_orden.html')
            #punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario=User.objects.get(id=request.user.id)
            now = datetime.now()
            estado=self.kwargs.get('estado')
            if (estado =='TODAS'):
                ordenes=OrdenElaboracion.objects.filter(fecha_emision__range=(self.kwargs.get('start'), self.kwargs.get('end')))
            else:
                ordenes=OrdenElaboracion.objects.filter(estado=self.kwargs.get('estado'),fecha_emision__range=(self.kwargs.get('start'), self.kwargs.get('end')))
            context = {
                'ordenes': ordenes,
                'usuario': usuario.username,
        
                'start': self.kwargs.get('start'),
                'end': self.kwargs.get('end'),

                'fecha': date.today().strftime("%d/%m/%Y"),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,

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
        except Exception as e:
                print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('ventas:factura_list'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context