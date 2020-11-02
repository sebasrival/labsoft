from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import PagoForm,PagoCuotaForm
from .models import Pago,PagoCuota
import datetime

# Create your views here.

@login_required()
@permission_required('pagos.add_pago', raise_exception=True)
def registrar_pago(request):
    form = PagoForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = PagoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El pago ha sido registrado correctamente!")
            generar_cuotas(form)
            return redirect('/pago/list/')
    context = {'form': form}
    return render(request, 'registrar_pago.html', context)


@login_required()
@permission_required('pagos.change_pago', raise_exception=True)
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
        else:
            messages.error(request, form.errors)

    context = {'form': form}

    return render(request, 'editar_pago.html', context)


@login_required()   
def editar_cuota(request, id):
    cuota = PagoCuota.objects.get(id=id)
    form = PagoCuotaForm(instance=cuota)
    if request.method == 'POST':
        cuota.estado=request.POST['estado']
        cuota.fecha_pago=datetime.date.today()
        cuota.save()
        pendientes=PagoCuota.objects.filter(id_pago_id=form.instance.id_pago_id).filter(estado='PENDIENTE').count()
        if pendientes==0:
            pago=Pago.objects.get(id=form.instance.id_pago_id)
            pago.estado='FINALIZADO'
            pago.save()
        messages.add_message(request, messages.SUCCESS, 'La cuota se ha editado correctamente!')
        return redirect('/pago/list')
       

    context = {'form': form}
    return render(request, 'editar_cuota.html', context)

@login_required()
@permission_required('pagos.delete_pago', raise_exception=True)
def delete_pago(request, id):
    pago= Pago.objects.get(id=id)
    pago.delete()
    return redirect('/pago/list/')


@login_required()
@permission_required('pagos.view_pago', raise_exception=True)
def lista_pagos(request):
    pagos = Pago.objects.all()
    context = {'pagos': pagos}
    return render(request, 'lista_pagos.html', context)

@login_required()
def lista_cuotas(request,id):
    cuotas = PagoCuota.objects.filter(id_pago_id=id)
    context = {'cuotas': cuotas}
    return render(request, 'lista_cuotas.html', context)



def generar_cuotas(form):
    dias=0
    for c in range(form.instance.cantidad_cuotas):
        cuota=PagoCuota()
        cuota.id_pago_id=form.instance.id
        cuota.estado='PENDIENTE'
        dias=dias+30
        cuota.fecha_vencimiento=datetime.date.today()+datetime.timedelta(days=dias)
        cuota.monto_cuota=(form.instance.monto_total)/(form.instance.cantidad_cuotas)
        cuota.save()
