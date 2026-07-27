from django.http import HttpResponse
from django.urls import path
from . import views
from django.shortcuts import render
import xmlrpc.client


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
]
URL = "http://localhost:8000"
DB = "mi_base"
USERNAME = "xavier1707"
PASSWORD = "xavier1707"


def conectar_odoo():
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, USERNAME, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    return uid, models


def lista_categoria(request):
    return render(request, "inventario/categoria.html")


def lista_productos(request):
    return render(request, "inventario/productos.html")


def lista_arte(request):
    return render(request, "inventario/artes.html")

app_name = 'inventario'

urlpatterns = [
    path('categoria/', views.lista_categoria, name='categoria'),
    path('producto/', views.lista_productos, name='lista_productos'),  # ← nueva
    path('artes/', views.lista_arte, name='lista_arte'),

]
def lista_categoria(request):
    return HttpResponse("Página de categorías")


def lista_productos(request):
    return HttpResponse("Página de productos")


def lista_arte(request):
    return HttpResponse("Página de artes")