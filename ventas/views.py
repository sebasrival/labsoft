import json
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ventas.forms import FacturaForm

# Create your views here.
from ventas.models import VentasConf, Factura, FacturaDetalle


@login_required()
@permission_required('ventas.view_factura', raise_exception=True)
def list_factura(request):
    facturas = Factura.objects.all()
    context = {'facturas': facturas }
    return render(request, 'lista_factura.html', context)

@login_required()
@permission_required('ventas.delete_factura', raise_exception=True)
def delete_factura(request, id):
    factura = Factura.objects.get(id=id)
    factura.delete()
    return redirect('/factura/list')


def get_detalle_factura(id):
    data = []
    try:
        detalles = FacturaDetalle.objects.filter(factura_id=id)
        for i in detalles:
            item = i.producto.obtener_dict()
            item['description'] = i.descripcion
            item['cantidad'] = i.cantidad
            data.append(item)
    except:
        pass
    return data


@login_required()
@permission_required('ventas.change_factura', raise_exception=True)
def editar_factura(request, id):
    data = {}
    fact = Factura.objects.get(id=id)
    form = FacturaForm(instance=fact)
    if request.method == 'POST' and request.is_ajax():
        try:
            factura_dict = json.loads(request.POST['factura'])
            print(factura_dict)
            try:
                factura = Factura.objects.get(id=id)
                factura.nro_factura = factura_dict['nro_factura']
                factura.cliente_id = factura_dict['cliente']
                factura.fecha_emision = datetime.strptime(factura_dict['fecha_emision'], "%d/%m/%Y")
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                factura.save()
                factura.facturadetalle_set.all().delete()
                for i in factura_dict['products']:
                    detalle = FacturaDetalle()
                    detalle.factura_id = factura.id
                    detalle.producto_id = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    context = {'form': form, 'det': json.dumps(get_detalle_factura(id))}
    return render(request, 'edit_factura.html', context)

@login_required()
@permission_required('ventas.add_factura', raise_exception=True)
def agregar_factura(request):
    form = FacturaForm()
    ventas_conf = get_config_ventas()
    data = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            factura_dict = json.loads(request.POST['factura'])
            #print(factura_dict)
            try:
                factura = Factura()
                factura.nro_factura = factura_dict['nro_factura']
                factura.cliente_id = factura_dict['cliente']
                factura.fecha_emision = datetime.strptime(factura_dict['fecha_emision'],"%d/%m/%Y")
                factura.estado = 'PENDIENTE'
                factura.total_iva = int(factura_dict['total_iva'])
                factura.total = int(factura_dict['total_factura'])
                #print("xd ",factura)
                factura.save()
                for i in factura_dict['products']:
                    detalle = FacturaDetalle()
                    detalle.factura_id = factura.id
                    detalle.producto_id = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    detalle.descripcion = i['description']
                    detalle.save()
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    contex = {'form': form, 'calc_iva': ventas_conf.calc_iva}

    return render(request, 'factura.html', contex)

def get_config_ventas():
    conf = VentasConf.objects.first()
    if conf:
        return VentasConf.objects.first()
    else:
        conf = VentasConf()
        conf.save()
    return conf