from django.shortcuts import render
from .models import Clientes,Reservas,Inventario,Gestion_reservas,Paquete

# Create your views here.

def vista_Clientes(request):
    clientes = Clientes.objects.all()
    return render(request,'clientes.html',{'clientes': clientes})

def vista_Reservas(request):
    reservas = Reservas.objects.all()
    return render(request,'resvervas.html',{'reservas':reservas})