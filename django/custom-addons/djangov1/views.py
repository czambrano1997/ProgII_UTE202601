from django.shortcuts import render

# Create your views here.

def Clientes(request):
    clientes = Clientes.objects.all()
    return render(request,'clientes.html',{'clientes': clientes})