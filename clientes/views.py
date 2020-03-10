from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def agregar_cliente(request):
    return render(request, 'agregar_cliente.html')