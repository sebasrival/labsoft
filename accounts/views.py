from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import UserForm, UserFormChange
from accounts.models import User


@login_required()
def lista_usuarios(request):
    usuarios = User.objects.all()
    context = {'usuarios': usuarios,
               'title': 'Usuarios',
               'subtitle': 'Lista de Usuarios'
               }
    return render(request, 'lista_user.html', context)

@login_required()
def agregar_usuario(request):
    form = UserForm()
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = UserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "El usuario ha sido agregado correctamente!")
            return redirect('/user/list/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,
               'title': 'Usuarios',
               'subtitle': 'Agregar Usuario'}
    return render(request, 'agregar_usuario.html', context)

@login_required()
def editar_usuario(request, id):
    usuario = User.objects.get(id=id)
    form = UserFormChange(instance=usuario)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = UserFormChange(data=request.POST, files=request.FILES, instance=usuario)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/user/list/')
        if form.is_valid():
            form.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El Usuario se ha editado correctamente!')
            return redirect('/user/list/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,
               'title': 'Usuarios',
               'subtitle': 'Editar Usuario'}
    return render(request, 'editar_usuario.html', context)

@login_required()
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/user/list/')