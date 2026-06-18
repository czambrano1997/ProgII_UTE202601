from django.shortcuts import render
from .models import Cliente,Flor,Pedido,Proveedor,TipoFlor

def clientes(request):
    datos =  Cliente.objects.all()
    return render(request, 'clientes.html',
                  {'datos':datos})

def flores(request):
    datos = Flor,object.all()
    return render(request, 'flores.html',
                  {'datos':datos})

def pedidos(request):
    datos = Pedido.objects.all()
    return render(request, 'pedidos.html',
                  {'datos': datos})

def proveedores(request):
    datos = Proveedor.objects.all()
    return render(request, 'proveedores.html',
                  {'datos': datos})

def tipo_flores(request):
    datos = TipoFlor.objects.all()
    return render(request, 'tipo_flores.html',
                  {'datos': datos})