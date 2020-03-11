from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto

# Create your views here.
@login_required()
def agregar_producto(request):
    form = ProductoForm
    if request.method =='POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar_producto')

    context = {'form':form}
    return render(request, 'agregar_producto.html', context)

@login_required()
def lista_producto(request):
    productos = Producto.objects.all()
    context = { 'productos': productos }
    return render(request, 'lista_producto.html', context)