import json

# from django.contrib import messages
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
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