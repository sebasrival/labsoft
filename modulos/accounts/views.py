from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

# Create your views here.
from modulos.accounts.forms import UserForm, UserFormChange, GroupForm, GroupChangeForm
from modulos.accounts.models import User
from django.contrib.auth.models import Group
from modulos.accounts.decorators import allowed_users

@login_required()
@allowed_users('accounts.view_user')
def lista_usuarios(request):
    usuarios = User.objects.all()
    context = {'usuarios': usuarios,
               'title': 'Usuarios',
               'subtitle': 'Lista de Usuarios'
               }
    return render(request, 'lista_user.html', context)

@login_required()
@allowed_users('accounts.add_user')
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
@allowed_users('accounts.change_user')
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
@allowed_users('accounts.delete_user')
def delete_user(request, id):
    user = User.objects.get(id=id)
    confirm = True
    if request.user == user:
        messages.error(request, "¡No puedes eliminar tu usuario! Contactar con el soporte técnico.")
        confirm = False
        return redirect('/user/list/')
    else:
        user.delete()
    context = {
        'confirm': confirm,
    }
    return render(request, "lista_user.html", context)

#grupos
@login_required()
@allowed_users(('auth.add_group', 'auth.view_group'))
def agregar_rol(request):
    form = GroupForm()
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = GroupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "El rol ha sido agregado correctamente!")
            return redirect('/rol/add/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,
               'title': 'Roles',
               'subtitle': 'Agregar Rol',
               'subtitle2': 'Lista de Roles',
               'groups': Group.objects.all()
               }
    return render(request, 'agregar_rol.html', context)

@login_required()
@allowed_users('auth.change_group')
def editar_rol(request, id):
    group = Group.objects.get(id=id)
    form = GroupChangeForm(instance=group)
    if request.method == 'POST':
        print("Imprimiendo POST: ", request.POST)
        form = GroupChangeForm(data=request.POST, instance=group)
        if not form.has_changed():
            messages.info(request, "No ha hecho ningun cambio")
            return redirect('/rol/add')
        if form.is_valid():
            form.save()
            # messages.success(request, "El cliente ha sido editado correctamente!")
            messages.add_message(request, messages.SUCCESS, 'El rol se ha editado correctamente!')
            return redirect('/rol/add/')
        else:
            messages.error(request, form.errors)

    context = {'form': form,
               'title': 'Roles',
               'subtitle': 'Editar Rol',
               'subtitle2': 'Lista Roles',
               'groups': Group.objects.all()}

    return render(request, 'agregar_rol.html', context)

@login_required()
@allowed_users(('auth.delete_group', 'auth.add_group'))
def delete_rol(request, id):
    group = Group.objects.get(id=id)
    group.delete()
    return redirect('/rol/add')
