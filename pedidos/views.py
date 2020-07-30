import json

# from django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import PedidoForm
from .models import Pedido, PedidoDetalle


# Create your views here.

@login_required()
def agregar_pedido(request):
    form = PedidoForm()
    data = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            pedidos_dict = json.loads(request.POST['pedidos'])
            print(pedidos_dict)
            try:
                pedido = Pedido()
                pedido.cliente_id = pedidos_dict['cliente'] # 15/06/2020
                pedido.fecha_pedido = datetime.strptime(pedidos_dict['fecha_pedido'], '%d/%m/%Y')
                pedido.fecha_entrega = datetime.strptime(pedidos_dict['fecha_entrega'], '%d/%m/%Y')
                pedido.estado = 'PENDIENTE'
                print(pedido)
                pedido.save()
                for i in pedidos_dict['products']:
                    detalle = PedidoDetalle()
                    detalle.pedido_id = pedido.id
                    detalle.producto_id = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    print(detalle.producto)
                    detalle.save()
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    context = {'form': form}
    return render(request, 'pedido_add.html', context)

@login_required()
def list_pedido(request):
    pedidos = Pedido.objects.all()
    context = { 'pedidos': pedidos }
    return render(request, 'lista_pedido.html',context)

@login_required()
def delete_pedido(request, id):
    pedido = Pedido.objects.get(id=id)
    pedido.delete()
    return redirect('/pedido/list')

@login_required()
def editar_pedido(request, id):
    data = {}
    ped = Pedido.objects.get(id=id)
    form = PedidoForm(instance=ped)
    if request.method == 'POST' and request.is_ajax():
        try:
            pedidos_dict = json.loads(request.POST['pedidos'])
            print(pedidos_dict)
            try:
                pedido = Pedido.objects.get(id=id)
                pedido.cliente_id = pedidos_dict['cliente']
                pedido.fecha_pedido = datetime.strptime(pedidos_dict['fecha_pedido'], '%d/%m/%Y')
                pedido.fecha_entrega = datetime.strptime(pedidos_dict['fecha_entrega'], '%d/%m/%Y')
                pedido.estado = 'PENDIENTE'
                print(pedido)
                pedido.save()
                pedido.pedidodetalle_set.all().delete()
                for i in pedidos_dict['products']:
                    detalle = PedidoDetalle()
                    detalle.pedido_id = pedido.id
                    detalle.producto_id = i['codigo_producto']
                    detalle.cantidad = int(i['cantidad'])
                    print(detalle.producto)
                    detalle.save()
            except Exception as e:
                print(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    context = { 'form': form, 'det':json.dumps(get_detalle_pedido(id))}
    return render(request, 'edit_pedido.html', context)

def get_detalle_pedido(id):
    data = []
    try:
        detalles = PedidoDetalle.objects.filter(pedido_id=id)
        for i in detalles:
            item = i.producto.obtener_dict()
            item['cantidad'] = i.cantidad
            data.append(item)
    except:
        pass
    return data