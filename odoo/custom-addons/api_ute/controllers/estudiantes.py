import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ApiEstudiantes(http.Controller):

    # Ajustado a /estudiantes/all para coincidir con Django
    @http.route('/api_ute/estudiantes/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_estudiantes(self, **kwargs):
        try:
            estudiantes = request.env['students.ute'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'surnames', 'age', 'phone', 'vat', 'grade_ids'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Estudiantes obtenidos', 'data': estudiantes}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo estudiantes')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    # Ajustado a /estudiantes/create
    @http.route('/api_ute/estudiantes/create', type='http', auth='public', methods=['POST'], csrf=False)
    def crear_estudiantes(self, **kwargs):
        """Creación de un nuevo estudiante por una app externa."""
        try:
            body = json.loads(request.httprequest.data)
            vals = {
                'name': body.get('name'),
                'surnames': body.get('surnames'),
                'age': body.get('age'),
                'phone': body.get('phone'),
                'vat': body.get('vat'),
            }
            if body.get('grade_ids'):
                vals['grade_ids'] = [(6, 0, body.get('grade_ids'))]
                
            record = request.env['students.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Estudiante creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando datos')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    # Ajustado a /estudiantes/delete/<id>
    @http.route('/api_ute/estudiantes/delete/<int:student_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def eliminar_estudiante(self, student_id, **kwargs):
        try:
            record = request.env['students.ute'].sudo().browse(student_id)
            if not record.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Estudiante no encontrado'}, default=str),
                    status=404,
                    headers=[('Content-Type', 'application/json')]
                )
            record.unlink()
            return request.make_response(
                json.dumps({'status': 'success', 'message': f'Estudiante {student_id} eliminado'}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error eliminando estudiante')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )