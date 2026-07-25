import json

import requests
from requests.exceptions import RequestException

ODOO_BASE = 'http://localhost:8069'
HEADERS = {'Content-Type': 'application/json'}
MODEL_KEYS = ['signature', 'usuarios', 'carrera', 'periodo', 'aula']


def build_url(model, action):
    return f"{ODOO_BASE}/api_ute/{model}/{action}"


def obtener_todos(model):
    try:
        url = build_url(model, 'all')
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        payload = response.json()
        if payload.get('status') != 'success':
            return {'error': payload.get('message', 'Error en Odoo'), 'data': []}
        return {'data': payload.get('data', [])}
    except (RequestException, ValueError) as exc:
        return {'error': f'No fue posible conectar con Odoo: {exc}', 'data': []}


def crear_registro(model, data):
    try:
        url = build_url(model, 'create')
        response = requests.post(url, headers=HEADERS, data=json.dumps(data), timeout=5)
        response.raise_for_status()
        payload = response.json()
        if payload.get('status') != 'success':
            return {'error': payload.get('message', 'Error al crear en Odoo'), 'data': []}
        return {'data': payload.get('data', {})}
    except (RequestException, ValueError) as exc:
        return {'error': f'No fue posible conectar con Odoo: {exc}', 'data': []}


def eliminar_registro(model, record_id):
    try:
        url = build_url(model, f'delete/{record_id}')
        response = requests.delete(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        payload = response.json()
        if payload.get('status') != 'success':
            return {'error': payload.get('message', 'Error al eliminar en Odoo'), 'data': []}
        return {'data': payload.get('data', {})}
    except (RequestException, ValueError) as exc:
        return {'error': f'No fue posible conectar con Odoo: {exc}', 'data': []}
