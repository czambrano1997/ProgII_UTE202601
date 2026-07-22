import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class StudentController(http.Controller):

    @http.route('/api_ute/estudiantes/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_students(self, **kwargs):
        try:
            students = request.env['students.ute'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'surnames', 'age', 'phone', 'vat'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Estudiantes obtenidos', 'data': students}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo estudiantes')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/estudiantes/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_student(self, **kwargs):
        try:
            raw_data = request.httprequest.data
            if raw_data:
                body = json.loads(raw_data.decode('utf-8'))
            else:
                body = kwargs

            # Valores por defecto para evitar restricciones NotNull en PostgreSQL
            vals = {
                'name': body.get('name') or body.get('nombre') or 'Sin Nombre',
                'surnames': body.get('surnames') or body.get('last_name') or body.get('apellidos') or 'Sin Apellido',
                'age': int(body.get('age', 18)),
                'phone': str(body.get('phone', '0999999999')),
                'vat': body.get('vat') or body.get('ci') or '0000000000000',
            }

            record = request.env['students.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Estudiante creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando estudiante')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/estudiantes/delete/<int:student_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_student(self, student_id, **kwargs):
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