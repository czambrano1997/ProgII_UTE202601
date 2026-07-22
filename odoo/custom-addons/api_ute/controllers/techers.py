import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class TeacherController(http.Controller):

    @http.route('/api_ute/techers/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_teachers(self, **kwargs):
        try:
            teachers = request.env['ou.teacher'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'last_name', 'email', 'phone', 'vat', 'validate_email', 'signature_primary'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Docentes obtenidos', 'data': teachers}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo docentes')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/techers/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_teacher(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data)
            vals = {
                'name': body.get('name'),
                'last_name': body.get('last_name'),
                'email': body.get('email'),
                'phone': body.get('phone'),
                'vat': body.get('vat'),
                'signature_primary': int(body.get('signature_primary')) if body.get('signature_primary') else False,
            }
            record = request.env['ou.teacher'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Docente creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando docente')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )