import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class SignatureController(http.Controller):

    @http.route('/api_ute/signature/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_signatures(self, **kwargs):
        try:
            signatures = request.env['ou.signature'].sudo().search_read(
                domain=[],
                fields=['id', 'name'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Materias obtenidas', 'data': signatures}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo materias')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/signature/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_signature(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data)
            record = request.env['ou.signature'].sudo().create({'name': body.get('name')})
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Materia creada', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando materia')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )