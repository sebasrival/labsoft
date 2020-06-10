from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PedidoForm


# Create your views here.
@login_required()
def agregar_pedido(request):
    form = PedidoForm()
    if request.method == 'POST':
        form = PedidoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El Pedido ha sido creado correctamente!")
            return redirect('index')
    context = {'form': form}
    return render(request, 'pedido_add.html', context)
