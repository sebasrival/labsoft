from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .forms import ProductoForm
from .models import Producto


# Create your views here.
@login_required()
@permission_required('productos.add_producto', raise_exception=True)
def agregar_producto(request):
    form = ProductoForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProductoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El producto ha sido creado correctamente!")
            return redirect('/product/list/')

    context = {'form': form}
    return render(request, 'agregar_producto.html', context)


@login_required()
@permission_required('productos.change_producto', raise_exception=True)
def editar_producto(request, id):
    producto = Producto.objects.get(codigo_producto=id)
    form = ProductoForm(instance=producto)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProductoForm(request.POST, instance=producto)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/product/list/')
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            messages.success(request, "El producto ha sido editado correctamente!")
            return redirect('/product/list/')

    context = {'form': form}
    return render(request, 'editar_producto.html', context)


@login_required()
@permission_required('productos.delete_producto', raise_exception=True)
def delete_producto(request, id):
    producto = Producto.objects.get(codigo_producto=id)
    producto.delete()
    return redirect('/product/list/')


@login_required()
@permission_required('productos.view_producto', raise_exception=True)
def lista_producto(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'lista_producto.html', context)

@login_required()
@permission_required('productos.view_producto', raise_exception=True)
@csrf_exempt
def search_products(request):
    data = {}
    try:
        print(request.method)
        print(request.POST['action'])
        term = request.POST['term']
        print(term)
        if (request.method == 'POST') and (request.POST['action'] == 'search_products'):
            print('entra')
            data = []
            prods = Producto.objects.filter(nombre__icontains=term)[0:10]
            print(prods, term)
            for p in prods:
                item = p.obtener_dict()
                item['id'] = p.codigo_producto
                producto_desc = '%s %s %s %s' % (p.nombre,
                                                 '' if p.color == '' else ' -- Color: ' + p.color,
                                                 '' if p.volumen == '' else ' -- Volumen: ' + str(int(p.volumen)),
                                                 ' -- Cantidad Neto: ' + str(int(p.cantidad_neto)))
                item['text'] = producto_desc
                data.append(item)
    except Exception as e:
        data['error'] = str(e)

    return JsonResponse(data, safe=False)
