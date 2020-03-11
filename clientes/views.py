from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from .models import Cliente

# Create your views here.

@login_required()
def agregar_cliente(request):
    form = ClienteForm
    if request.method =='POST':
        print("Imprimiendo POST: ", request.POST)
        form = ClienteForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/agregar_cliente')

    context = {'form':form}
    return render(request, 'agregar_cliente.html', context)

@login_required()
def lista_cliente(request):
    clientes = Cliente.objects.all()
    context = { 'clientes': clientes }
    return render(request, 'lista_cliente.html', context)