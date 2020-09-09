from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import PagoForm
from .models import Pago


# Create your views here.

@login_required()
def registrar_pago(request):
    form = PagoForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = PagoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El pago ha sido registrado correctamente!")
            return redirect('/pago/list/')

    context = {'form': form}
    return render(request, 'registrar_pago.html', context)


@login_required()
def editar_pago(request, id):
    pago = Pago.objects.get(id=id)
    form = PagoForm(instance=pago)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = PagoForm(request.POST, instance=pago)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/pago/list/')
        if form.is_valid():
            pago = form.save(commit=False)
            pago.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El pago se ha editado correctamente!')
            return redirect('/pago/list/')

    context = {'form': form}
    return render(request, 'editar_pago.html', context)


@login_required()
def delete_pago(request, id):
    pago= Pago.objects.get(id=id)
    pago.delete()
    return redirect('/pago/list/')


@login_required()
def lista_pagos(request):
    pagos = Pago.objects.all()
    context = {'pagos': pagos}
    return render(request, 'lista_pagos.html', context)

