import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LibraryController(http.Controller):

    @http.route('/api_ute/library/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_libraries(self, **kwargs):
        try:
            records = request.env['library.ute'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'author', 'headquarters', 'hous', 'gender', 'income'],
            )
            return request.make_response(
                # Se agrega default=str para convertir objetos date/datetime a string
                json.dumps({'status': 'success', 'message': 'Libros obtenidos', 'data': records}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error al consultar libros')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/library/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_library(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data)
            vals = {
                'name': body.get('name'),
                'author': body.get('author'),
                'headquarters': body.get('headquarters'),
                'hous': body.get('hous'),
                'gender': body.get('gender'),
                'income': body.get('income'),
            }
            record = request.env['library.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Libro creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando el registro')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/library/delete/<int:library_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_library(self, library_id, **kwargs):
        try:
            record = request.env['library.ute'].sudo().browse(library_id)
            if not record.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Libro no encontrado'}, default=str),
                    status=404,
                    headers=[('Content-Type', 'application/json')]
                )
            record.unlink()
            return request.make_response(
                json.dumps({'status': 'success', 'message': f'Libro {library_id} eliminado'}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error eliminando el registro')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )