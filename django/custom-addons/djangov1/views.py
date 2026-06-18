from django.shortcuts import render
from .models import Clientes,Reservas,Inventario,Gestion_reservas,Paquete

# Create your views here.

def vista_Clientes(request):
    clientes = Clientes.objects.all()
    return render(request,'clientes.html',{'clientes': clientes})

def vista_Reservas(request):
    reservas = Reservas.objects.all()
    return render(request,'resvervas.html',{'reservas':reservas})

def vista_Inventario(request):
    inventario = Inventario.objects.all()
    return render(request,'inventario.html',{'inventario':inventario})

def vista_Gestion(request):
    gestion_reservas = Gestion_reservas.objects.all()
    return render(request,'gestion_reservas.html',{'gestion_reservas':gestion_reservas})

def vista_paquetes(request):
    paquete = Paquete.objects.all()
    return render(request,'paquete.html',{'paquete':paquete})