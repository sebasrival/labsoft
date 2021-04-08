from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProveedorForm
from .models import Proveedor
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

@login_required()
def agregar_proveedor(request):
    form = ProveedorForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProveedorForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El proveedor ha sido agregado correctamente!")
            return redirect('/proveedor/list/')

    context = {'form': form}
    return render(request, 'agregar_proveedor.html', context)


@login_required()
def editar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    form = ProveedorForm(instance=proveedor)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ProveedorForm(request.POST, instance=proveedor)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/proveedor/list/')
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El Proveedor se ha editado correctamente!')
            return redirect('/proveedor/list/')

    context = {'form': form}
    return render(request, 'editar_proveedor.html', context)


@login_required()
def delete_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)
    proveedor.delete()
    return redirect('/proveedor/list/')


@login_required()
def lista_proveedor(request):
    proveedores = Proveedor.objects.all()
    context = {'proveedores': proveedores}
    return render(request, 'lista_proveedor.html', context)
