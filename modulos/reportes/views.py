

from django.db.models import Q


from modulos.compras.models import FacturaCompra, FacturaDet, StockMateriaPrima, MateriaPrima
from modulos.reportes.forms import ReporteFiltro, MesForm
import os
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
from django.http import HttpResponseRedirect
from django.template.loader import get_template


# Create your views here.

def PantallaReporteVenta(request):
    ANHIOS = [ ('2018', 2018),
        ('2019', 2019),
        ('2020', 2020),
        ('2021', 2021),
        ('2022', 2022),
        ('2023', 2023),

        ]
    
    
    context = {
        'anhos' : ANHIOS,

    }
    return render(request, "ventas/venta_filtro.html",context)


def PantallaReporteOrden(request):
    return render(request, "produccion/generar_reporte_orden.html")


def PantallaReporteVentaMensual(request):
    MESES = [
        ('Enero', 1),
        ('Febrero', 2),
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
    ANHIOS = [ ('2018', 2018),
        ('2019', 2019),
        ('2020', 2020),
        ('2021', 2021),
        ('2022', 2022),
        ('2023', 2023),

        ]
    
    
    context = {
        'meses': MESES,
        'anhos' : ANHIOS,

    }
    return render(request, "ventas/generar_reporte_mensual.html", context)


def PantallaReporteProductoMensual(request):
    MESES = [
        ('Enero', 1),
        ('Febrero', 2),
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
    ANHIOS = [ ('2018', 2018),
        ('2019', 2019),
        ('2020', 2020),
        ('2021', 2021),
        ('2022', 2022),
        ('2023', 2023),

        ]
    
    context = {
        'meses': MESES,
        'anhos': ANHIOS

    }
    return render(request, "produccion/generar_productos_mensual.html", context)


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
            # punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario = User.objects.get(id=request.user.id)
            print(usuario)
            now = datetime.now()
            print("La hora actual es {}".format(now.hour))

            context = {
                # 'datos_facturacion': DatosFacturacion.objects.get(punto_venta=punto_venta.codigo),
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
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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
            # punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            facturas = FacturaVenta.objects.all()
            usuario = User.objects.get(id=request.user.id)
            now = datetime.now()
            factura = FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')).count()
            print(factura)
            facturas=FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year'))
            if factura == 0:

                total_facturas = 0
                total_exentas = 0
                total_montoiva1 = 0
                total_montoiva2 = 0
                total_gravadas10 = 0
                total_gravadas5 = 0
                total_sin_iva = 0
            else:
                total_facturas = round(
                    FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')).aggregate(
                        Sum('total')).get('total__sum'))
                total_exentas = round(
                    FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')).aggregate(
                        Sum('exenta')).get('exenta__sum'))
                total_montoiva1 = round(
                    FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')).aggregate(
                        Sum('monto_iva1')).get('monto_iva1__sum'))
                total_montoiva2 = round(
                    FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')).aggregate(
                        Sum('monto_iva2')).get('monto_iva2__sum'))

            total_gravadas5=0
            total_gravadas10=0
            total_sin_iva=0
            print(facturas)
            for f in facturas:
                total_gravadas10 += f.obtener_gravada_10()
                total_gravadas5 +=f.obtener_gravada_5()
            total_sin_iva= (total_gravadas10 - total_montoiva1) + (total_gravadas5 - total_montoiva2)
            context = {
                'facturas': FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year')),
                'usuario': usuario.username,
                'total_ventas': f'{total_facturas:,.0f}',
                'total_exentas': f'{total_exentas:,.0f}',
                'total_montoiva1': f'{total_montoiva1:,.0f}',
                'total_montoiva2': f'{total_montoiva2:,.0f}',
                'total_gravadas10': f'{total_gravadas10:,.0f}',
                'total_gravadas5': f'{total_gravadas5:,.0f}',
                'total_sin_iva': f'{total_sin_iva:,.0f}',
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
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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
        MESES = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE',
                 'NOVIEMBRE', 'DICIEMBRE']

        try:
            template = get_template('ventas/reporte_venta_mensual.html')
            # punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            facturas = FacturaVenta.objects.all()
            usuario = User.objects.get(id=request.user.id)
            now = datetime.now()
            factura = FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year'),
                                                  fecha_emision__month=self.kwargs.get('mes')).count()
            print(factura)
            facturas=FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year'),
                                                        fecha_emision__month=self.kwargs.get('mes'))
            if factura == 0:

                total_facturas = 0
                total_exentas = 0
                total_montoiva1 = 0
                total_montoiva2 = 0
                total_gravadas10 = 0
                total_gravadas5 = 0
                total_sin_iva = 0
            else:
                total_facturas = round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                   fecha_emision__month=self.kwargs.get('mes'),
                                                                   estado='PAGADA').aggregate(Sum('total')).get(
                    'total__sum'))
                total_exentas = round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                  fecha_emision__month=self.kwargs.get('mes'),
                                                                  estado='PAGADA').aggregate(Sum('exenta')).get(
                    'exenta__sum'))
                total_montoiva1 = round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                    fecha_emision__month=self.kwargs.get('mes'),
                                                                    estado='PAGADA').aggregate(Sum('monto_iva1')).get(
                    'monto_iva1__sum'))
                total_montoiva2 = round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                    fecha_emision__month=self.kwargs.get('mes'),
                                                                    estado='PAGADA').aggregate(Sum('monto_iva2')).get(
                    'monto_iva2__sum'))
                total_gravadas10 = round(float(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                           fecha_emision__month=self.kwargs.get('mes'),
                                                                           estado='PAGADA').aggregate(
                    Sum('monto_iva1')).get('monto_iva1__sum')) * 11)
                total_gravadas5 = round(FacturaVenta.objects.filter(fecha_emision__year=self.kwargs.get('year'),
                                                                    fecha_emision__month=self.kwargs.get('mes'),
                                                                    estado='PAGADA').aggregate(Sum('monto_iva2')).get(
                    'monto_iva2__sum') * 21)
            total_gravadas5=0
            total_gravadas10=0
            total_sin_iva=0
            print(facturas)
            for f in facturas:
                total_gravadas10 += f.obtener_gravada_10()
                total_gravadas5 +=f.obtener_gravada_5()
            total_sin_iva= (total_gravadas10 - total_montoiva1) + (total_gravadas5 - total_montoiva2)

            context = {
                'facturas': FacturaVenta.objects.filter(estado='PAGADA', fecha_emision__year=self.kwargs.get('year'),
                                                        fecha_emision__month=self.kwargs.get('mes')),
                'usuario': usuario.username,
                'total_ventas': f'{total_facturas:,.0f}',
                'total_exentas': f'{total_exentas:,.0f}',
                'total_montoiva1': f'{total_montoiva1:,.0f}',
                'total_montoiva2': f'{total_montoiva2:,.0f}',
                'total_gravadas10': f'{total_gravadas10:,.0f}',
                'total_gravadas5': f'{total_gravadas5:,.0f}',
                'total_sin_iva': f'{total_sin_iva:,.0f}',
                'mes': MESES[self.kwargs.get('mes') - 1],
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
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except Exception as e:
            print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProductoReporte():
    codigo = ""
    nombre = ""
    cantidad_producida = 0
    cantidad_vendida = 0


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
        MESES = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE',
                 'NOVIEMBRE', 'DICIEMBRE']
        try:
            template = get_template('produccion/reporte_productos_mensual.html')
            # punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario = User.objects.get(id=request.user.id)
            now = datetime.now()

            vendida_total = 0
            producida_total = 0
            for producto in Producto.objects.all():
                p = ProductoReporte()
                p.codigo = producto.codigo_producto
                p.nombre = producto.nombre
                p.cantidad_producida = producto.obtener_cantidad_producida(self.kwargs.get('mes'),
                                                                           self.kwargs.get('year'))
                producida_total = producida_total + p.cantidad_producida
                p.cantidad_vendida = producto.obtener_cantidad_vendida(self.kwargs.get('mes'), self.kwargs.get('year'))
                vendida_total = vendida_total + p.cantidad_vendida

                PRODUCTOS.append(p)

            print(vendida_total)
            PRODUCTOS.sort(key=lambda x: x.cantidad_vendida, reverse=True)
            if (PRODUCTOS[0].cantidad_vendida == 0):
                mas_vendida = 'NINGUNO'
            else:
                mas_vendida = PRODUCTOS[0].nombre

            PRODUCTOS.sort(key=lambda x: x.cantidad_producida, reverse=True)
            if (PRODUCTOS[0].cantidad_producida == 0):
                mas_producida = 'NINGUNO'
            else:
                mas_producida = PRODUCTOS[0].nombre
            context = {
                'productos': Producto.objects.all(),
                'lista_producto': PRODUCTOS,
                'usuario': usuario.username,
                # 'total_ventas':f'{total_facturas:,.0f}',
                'mes': MESES[self.kwargs.get('mes') - 1],
                'anho': self.kwargs.get('year'),
                'usuario': usuario.username,
                'producida_total': int(producida_total),
                'vendida_total': vendida_total,
                'usuario': usuario.username,
                'mas_vendida': mas_vendida,
                'mas_producida': mas_producida,

                'fecha': date.today().strftime("%d/%m/%Y"),
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,

                'comp': {'name': 'LABORATORIO OCAMPOS SRL', 'ruc': '9999999999999', 'address': 'San Lorenzo, Paraguay'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except Exception as e:
            print(e)
        pass
        return HttpResponseRedirect(reverse_lazy('index'))

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
        MESES = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE',
                 'NOVIEMBRE', 'DICIEMBRE']

        try:
            template = get_template('produccion/reporte_orden.html')
            # punto_venta=PuntoVenta.objects.get(id=factura.punto_venta_id)
            usuario = User.objects.get(id=request.user.id)
            now = datetime.now()
            estado = self.kwargs.get('estado')
            if (estado == 'TODAS'):
                ordenes = OrdenElaboracion.objects.filter(
                    fecha_emision__range=(self.kwargs.get('start'), self.kwargs.get('end')))
            else:
                ordenes = OrdenElaboracion.objects.filter(estado=self.kwargs.get('estado'), fecha_emision__range=(
                self.kwargs.get('start'), self.kwargs.get('end')))
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
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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

class ReporteCompraPdfView(View):

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

    def post(self, request, *args, **kwargs):
        try:
            start_date = datetime.strptime(request.POST['start_date'], '%d/%m/%Y')
            end_date = datetime.strptime(request.POST['end_date'], '%d/%m/%Y')
            template = get_template('compras/reporte_compra_pdf.html')
            facturas = FacturaCompra.objects.filter(Q(estado='RECIBIDO') and Q(fecha_factura__range=[start_date, end_date]))
            user = User.objects.get(id=request.user.id)
            usuario = "%s %s" % (user.first_name, user.last_name)
            now = datetime.now()
            t = self.get_totales(facturas)
            context = {
                'facturas': facturas,
                'total': t['total_comprobante'],
                'total_exenta': t['total_exenta'],
                'total_grabada5': t['total_grabada5'],
                'total_iva5': t['total_iva5'],
                'total_grabada10': t['total_grabada10'],
                'total_iva10': t['total_iva10'],
                'usuario': usuario,
                'fecha': date.today().strftime("%d/%m/%Y"),
                'año': now.year,
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,
                'start_date': datetime.strftime(start_date, "%d/%m/%Y"),
                'end_date': datetime.strftime(end_date, "%d/%m/%Y"),
                'comp': {'name': 'LABORATORIO OCAMPOS SRL', 'ruc': '9999999999999', 'address': 'San Lorenzo, Paraguay'},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('index'))

    def get(self, request, *args, **kwargs):
        form = ReporteFiltro
        context = {'form': form,
                    'title': 'Reporte de Compras'}
        return render(request, 'compras/reporte_compras.html', context)

    def get_totales(self, facturas):
        dict = {
            'total_comprobante' : 0,
            'total_exenta' : 0,
            'total_grabada5' : 0,
            'total_iva5' : 0,
            'total_grabada10' : 0,
            'total_iva10': 0
        }
        for f in facturas:
            dict['total_comprobante'] += f.total
            dict['total_exenta'] += f.get_exenta()
            dict['total_grabada5'] += f.get_grabada5()
            dict['total_iva5'] += f.monto_iva1
            dict['total_grabada10'] += f.get_grabada10()
            dict['total_iva10'] += f.monto_iva2
        return dict


class ReporteMateriaPrima(View):

    def post(self, request, *args, **kwargs):
        try:
            mes = datetime.strptime(request.POST['mes'], "%m-%Y")
            facturas = FacturaCompra.objects.filter(Q(estado='recibido') and Q(fecha_factura__year=mes.year, fecha_factura__month=mes.month))
            materias = self.reporte_materia_utilizado(facturas)
            user = User.objects.get(id=request.user.id)
            usuario = "%s %s" % (user.first_name, user.last_name)
            now = datetime.now()
            template = get_template('compras/reporte_materia_prima.html')
            context = {
                'materias': materias,
                'usuario': usuario,
                'fecha': date.today().strftime("%d/%m/%Y"),
                'año': now.year,
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,
                'fecha_reporte': mes,
                'comp': {'name': 'LABORATORIO OCAMPOS SRL', 'ruc': '9999999999999', 'address': 'San Lorenzo, Paraguay'},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('index'))

    def get(self, request, *args, **kwargs):
        form = MesForm
        context = {'form': form,
                    'title': 'Reporte de Materias Primas'}
        return render(request, 'compras/reporte_materia_prima_form.html', context)

    def reporte_materia_utilizado(self, facturas):
        materias = []
        mts = MateriaPrima.objects.all()
        for m in mts:
            item = {}
            item['materia'] = m.nombre
            item['um'] = m.um
            item['cantidadCont'] = m.cantidadCont
            item['comprado_mes'] = 0
            for f in facturas:
                try:
                    det = FacturaDet.objects.get(factura=f, materia=m)
                    item['comprado_mes'] += det.cantidad
                except Exception as e:
                    pass
            materias.append(item)

        return materias

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