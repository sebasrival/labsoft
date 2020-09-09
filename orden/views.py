from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

# Create your views here.
from orden.forms import OrdenForm
from orden.models import OrdenElaboracion


@login_required()
@permission_required('orden.add_ordenelaboracion', raise_exception=True)
def agregar_orden(request):
    form = OrdenForm()
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = OrdenForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "El orden ha sido agregado correctamente!")
            return redirect('/orden/list/')
        else:
            messages.error(request, form.errors)

    context = {'form': form}
    return render(request, 'agregar_orden.html', context)


@login_required()
@permission_required('orden.change_ordenelaboracion', raise_exception=True)
def editar_orden(request, id):
    print("Hola")
    orden = OrdenElaboracion.objects.get(id=id)
    form = OrdenForm(instance=orden)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = OrdenForm(request.POST, instance=orden)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/orden/list/')
        if form.is_valid():
            orden = form.save(commit=False)
            orden.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El Orden se ha editado correctamente!')
            return redirect('/orden/list/')

    context = {'form': form}
    return render(request, 'editar_orden.html', context)


@login_required()
@permission_required('orden.delete_ordenelaboracion',raise_exception=True)
def delete_orden(request, id):
    orden = OrdenElaboracion.objects.get(id=id)
    orden.delete()
    return redirect('/orden/list/')


@login_required()
@permission_required('orden.view_ordenelaboracion', raise_exception=True)
def lista_orden(request):
    orden = OrdenElaboracion.objects.all()
    context = {'ordenes': orden}
    return render(request, 'lista_orden.html', context)