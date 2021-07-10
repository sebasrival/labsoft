from django.db.models import Q

from modulos.compras.models import FacturaCompra
from modulos.reportes.forms import ReporteFiltro
import os
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import View
from xhtml2pdf import pisa
from modulos.produccion.models import Equipo
from modulos.ventas.models import *

from modulos.accounts.models import User
from datetime import datetime
from datetime import date

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template


# Create your views here.
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
            total_facturas = round(FacturaVenta.objects.aggregate(Sum('total')).get('total__sum'))
            total_exentas = round(FacturaVenta.objects.aggregate(Sum('exenta')).get('exenta__sum'))
            total_montoiva1 = round(FacturaVenta.objects.aggregate(Sum('monto_iva1')).get('monto_iva1__sum'))
            total_montoiva2 = round(FacturaVenta.objects.aggregate(Sum('monto_iva2')).get('monto_iva2__sum'))
            total_gravadas10 = round(
                float(FacturaVenta.objects.aggregate(Sum('monto_iva1')).get('monto_iva1__sum')) * 11)
            total_gravadas5 = round(FacturaVenta.objects.aggregate(Sum('monto_iva2')).get('monto_iva2__sum') * 21)
            total_sin_iva = (total_gravadas10 - total_montoiva1) + (total_gravadas5 - total_montoiva2)
            context = {
                'facturas': FacturaVenta.objects.all(),
                'usuario': usuario.username,
                'total_ventas': f'{total_facturas:,.0f}',
                'total_exentas': f'{total_exentas:,.0f}',
                'total_montoiva1': f'{total_montoiva1:,.0f}',
                'total_montoiva2': f'{total_montoiva2:,.0f}',
                'total_gravadas10': f'{total_gravadas10:,.0f}',
                'total_gravadas5': f'{total_gravadas5:,.0f}',
                'total_sin_iva': f'{total_sin_iva:,.0f}',

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
            facturas = FacturaCompra.objects.filter(Q(estado='RECIBIDO') | Q(fecha_factura__range=[start_date, end_date]))
            user = User.objects.get(id=request.user.id)
            usuario = "%s %s" % (user.first_name, user.last_name)
            now = datetime.now()
            context = {
                'facturas': facturas,
                'usuario': usuario,
                'fecha': date.today().strftime("%d/%m/%Y"),
                'año': now.year,
                'hora': now.hour,
                'minutos': now.minute,
                'segundos': now.second,
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
