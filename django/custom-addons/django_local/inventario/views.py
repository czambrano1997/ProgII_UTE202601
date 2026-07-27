from django.shortcuts import render

import xmlrpc.client
from django.shortcuts import render, redirect

# Vista de productos
def lista_productos(request):
    return render(request, 'inventario/productos.html')

# Vista de artes
def lista_arte(request):
    return render(request, 'inventario/artes.html')

# Funciones para vista categoria
def lista_categoria(request):
    return render(request, 'invetanverio/categoria.html')

def crear_cliente(request):

    url = 'http://localhost:8001'
    db = 'mi_base'
    username = 'xavier1707'
    password = 'xavier1707'

    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')

    uid = common.authenticate(db, username, password, {})

    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    models.execute_kw(
        db,
        uid,
        password,
        'res.partner',
        'create',
        [{
            'name': 'Cliente Django'
        }]
    )

    return redirect('/')