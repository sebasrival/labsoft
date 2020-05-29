from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductoForm
from .models import Producto
from django.contrib import messages

# Create your views here.
@login_required()
def agregar_producto(request):
    form = ProductoForm
    if request.method =='POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El producto ha sido creado correctamente!")
            return redirect('/lista_producto')

    context = {'form':form}
    return render(request, 'agregar_producto.html', context)

@login_required()
def editar_producto(request, id):
    producto = Producto.objects.get(codigo_producto=id)
    form = ProductoForm(instance=producto)
    if request.method =='POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProductoForm(request.POST, instance=producto)
        if not form.has_changed():
            messages.info(request,"No ha hecho ningun cambio")
            return redirect('/lista_producto')
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            messages.success(request, "El producto ha sido editado correctamente!")
            return redirect('/lista_producto')

    context = {'form':form}
    return render(request, 'editar_producto.html', context)

@login_required()
def delete_producto(request, id):
    producto = Producto.objects.get(codigo_producto=id)
    producto.delete()
    return redirect('/lista_producto')

@login_required()
def lista_producto(request):
    productos = Producto.objects.all()
    context = { 'productos': productos }
    return render(request, 'lista_producto.html', context)