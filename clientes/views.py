from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from .models import Cliente
from django.contrib import messages


# Create your views here.

@login_required()
def agregar_cliente(request):
    form = ClienteForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El cliente ha sido agregado correctamente!")
            return redirect('/cliente/list/')

    context = {'form': form}
    return render(request, 'agregar_cliente.html', context)


@login_required()
def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    form = ClienteForm(instance=cliente)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = ClienteForm(request.POST, instance=cliente)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/cliente/list/')
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El Cliente se ha editado correctamente!')
            return redirect('/cliente/list/')

    context = {'form': form}
    return render(request, 'editar_cliente.html', context)


@login_required()
def delete_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('/cliente/list/')


@login_required()
def lista_cliente(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'lista_cliente.html', context)
