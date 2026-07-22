from django.shortcuts import render

import xmlrpc.client
from django.shortcuts import render, redirect

# Funciones para vista categoria

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