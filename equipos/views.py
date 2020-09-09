from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import EquipoForm
from .models import Equipo


# Create your views here.

@login_required()
def agregar_equipo(request):
    form = EquipoForm
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = EquipoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El equipo ha sido registrado correctamente!")
            return redirect('/equipo/list/')

    context = {'form': form}
    return render(request, 'registrar_equipo.html', context)


@login_required()
def editar_equipo(request, id):
    equipo = Equipo.objects.get(id=id)
    form = EquipoForm(instance=equipo)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = EquipoForm(request.POST, instance=equipo)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/equipo/list/')
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El equipo se ha editado correctamente!')
            return redirect('/equipo/list/')

    context = {'form': form}
    return render(request, 'editar_equipo.html', context)


@login_required()
def delete_equipo(request, id):
    equipo = Equipo.objects.get(id=id)
    equipo.delete()
    return redirect('/equipo/list/')


@login_required()
def lista_equipos(request):
    equipos = Equipo.objects.all()
    context = {'equipos': equipos}
    return render(request, 'lista_equipos.html', context)

