from django.shortcuts import render, redirect
from django.forms import  modelformset_factory
from .models import Pedido, PedidoDetalle
from .forms import PedidoForm, PedidoDetalleForm

# Create your views here.
def agregar_pedido(request):
    PedidoDetalleSet = modelformset_factory(PedidoDetalle, form=PedidoDetalleForm)
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        formset = PedidoDetalleSet(request.POST, request.FILES, queryset=PedidoDetalle.objects.none())
        print('\n')
        print(' post: ',request.POST)
        print('files: ', request.FILES)
        print('\n')
        print('\n pedido: ', pedido_form.is_valid())
        print('\n detalle: ', formset.is_valid())
        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save(commit=False)
            pedido.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.pedido = pedido
                detalle.save()
            return redirect('/')
    else:
        pedido_form = PedidoForm()
        formset = PedidoDetalleSet(queryset=PedidoDetalle.objects.none())
    return render(request, 'agregar_pedido.html', {'formset':formset, 'pedido': pedido_form})