from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Producto,StockProductos
from .forms import ProductoForm

# Vistas de productos
class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_add.html'
    success_url = reverse_lazy('produccion:producto_list')


    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            response = ''
            try:
                form = self.get_form()
                # noinspection DuplicatedCode
                if form.is_valid():
                    form.save() 
                    data['message'] = f'¡{self.model.__name__} registrado correctamente!'
                    data['error'] = '¡Sin errores!'
                    response = JsonResponse(data, safe=False)
                    response.status_code = 201  # codigo de que esta bien
                    p=Producto.objects.get(codigo_producto=form['codigo_producto'].value())
                    s=StockProductos(cantidad=0,producto_id=p.id)
                    s.save()

                else:
                    data['message'] = '¡Los datos ingresados no son validos!'
                    data['error'] = form.errors
                    response = JsonResponse(data, safe=False)
                    response.status_code = 400  # codigo de que hay algo malo xd
            except Exception as e:
                data['error'] = str(e)
        
            return response
        else:
            return redirect('produccion:producto_list')
    



    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            return redirect('produccion:producto_list')

 
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/productos_list.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            try:
                data = []
                for prod in self.get_queryset():
                    stock=StockProductos.objects.get(producto_id=prod.id)
                    producto = {
                        'codigo_producto': prod.codigo_producto,
                        'nombre': prod.nombre,
                        'tipo': prod.tipo,
                        'color': prod.color,
                        'precio': prod.precio,
                        'cantidad_contenido': prod.cantidad_contenido,
                        'cantidad': stock.cantidad,
                        'id': prod.id
                    }
                    data.append(producto)
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data, safe=False)
        else:
            context = {
                'title': 'productos',
                'subtitle': 'Stock de productos',
                'route': reverse_lazy('produccion:producto_list'),
                'form': ProductoForm()
            }
            return render(request, self.template_name, context)


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/productos_edit.html'
    success_url = reverse_lazy('produccion:producto_list')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {}
            response = ''
            try:
                form = self.form_class(request.POST, instance=self.get_object())
                # noinspection DuplicatedCode
                if form.is_valid():
                    form.save()
                    data['message'] = f'¡{self.model.__name__} editado correctamente!'
                    data['error'] = '¡Sin errores!'
                    response = JsonResponse(data, safe=False)
                    response.status_code = 201  # codigo de que esta bien
                else:
                    data['message'] = '¡Los datos ingresados no son validos!'
                    data['error'] = form.errors
                    response = JsonResponse(data, safe=False)
                    response.status_code = 400  # codigo de que hay algo malo xd
            except Exception as e:
                data['error'] = str(e)
            return response
        else:
            return reverse_lazy('produccion:producto_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:producto_list')


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy('produccion:producto_list')

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return super().get(self, request, *args, **kwargs)
        else:
            # redirectcciona si se hace una peticion que no sea ajax
            return redirect('produccion:producto_list')

