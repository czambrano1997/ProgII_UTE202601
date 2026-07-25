import json

from odoo import http
from odoo.http import request


MODEL_MAP = {
    'signature': 'ou.signature',
    'usuarios': 'sistema.usuarios',
    'carrera': 'ou.carrera',
    'periodo': 'ou.periodo',
    'aula': 'ou.aula',
}

FIELD_MAP = {
    'signature': ['name'],
    'usuarios': ['name', 'last_name', 'email', 'phone', 'vat'],
    'carrera': ['name', 'codigo', 'modalidad'],
    'periodo': ['name', 'fecha_inicio', 'fecha_fin', 'activo'],
    'aula': ['name', 'edificio', 'capacidad'],
}


def json_response(payload, status_code=200):
    response = request.make_response(
        json.dumps(payload, default=str),
        headers=[('Content-Type', 'application/json')],
    )
    response.status_code = status_code
    return response


def parse_request_body():
    try:
        body = request.httprequest.get_data(as_text=True)
        if body:
            return json.loads(body)
    except ValueError:
        pass
    return dict(request.params)


class ApiUTEController(http.Controller):
    @staticmethod
    def get_model_name(model_key):
        if model_key not in MODEL_MAP:
            raise ValueError('Modelo inválido')
        return MODEL_MAP[model_key]

    @http.route('/api_ute/<string:model>/all', type='http', auth='public', methods=['GET'], csrf=False)
    def obtener_todos(self, model, **kwargs):
        try:
            model_name = self.get_model_name(model)
            records = request.env[model_name].sudo().search([])
            data = records.read(['id'] + FIELD_MAP[model])
            return json_response({'status': 'success', 'message': '', 'data': data})
        except Exception as exc:
            return json_response({'status': 'error', 'message': str(exc), 'data': []}, status_code=500)

    @http.route('/api_ute/<string:model>/create', type='http', auth='public', methods=['POST'], csrf=False)
    def crear_registro(self, model, **kwargs):
        try:
            model_name = self.get_model_name(model)
            payload = parse_request_body()
            values = {key: payload.get(key) for key in FIELD_MAP[model] if key in payload}
            if not values:
                return json_response({'status': 'error', 'message': 'No se enviaron datos de creación', 'data': []}, status_code=400)
            record = request.env[model_name].sudo().create(values)
            return json_response({'status': 'success', 'message': 'Registro creado', 'data': record.read(['id'] + FIELD_MAP[model])[0]})
        except Exception as exc:
            return json_response({'status': 'error', 'message': str(exc), 'data': []}, status_code=500)

    @http.route('/api_ute/<string:model>/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def eliminar_registro(self, model, record_id, **kwargs):
        try:
            model_name = self.get_model_name(model)
            record = request.env[model_name].sudo().browse(record_id)
            if not record.exists():
                return json_response({'status': 'error', 'message': 'Registro no encontrado', 'data': []}, status_code=404)
            record.sudo().unlink()
            return json_response({'status': 'success', 'message': 'Registro eliminado', 'data': {'id': record_id}})
        except Exception as exc:
            return json_response({'status': 'error', 'message': str(exc), 'data': []}, status_code=500)

