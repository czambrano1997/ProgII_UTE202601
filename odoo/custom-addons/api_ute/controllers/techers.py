import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class TeacherController(http.Controller):

    @http.route('/api_ute/techers/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_teachers(self, **kwargs):
        try:
            records = request.env['ou.teacher'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'last_name', 'email', 'phone', 'vat', 'validate_email', 'signature_primary'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Docentes obtenidos', 'data': records}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error al consultar docentes')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
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
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/techers/delete/<int:teacher_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_teacher(self, teacher_id, **kwargs):
        try:
            record = request.env['ou.teacher'].sudo().browse(teacher_id)
            if not record.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Docente no encontrado'}, default=str),
                    status=404,
                    headers=[('Content-Type', 'application/json')]
                )
            record.unlink()
            return request.make_response(
                json.dumps({'status': 'success', 'message': f'Docente {teacher_id} eliminado'}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error eliminando docente')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )