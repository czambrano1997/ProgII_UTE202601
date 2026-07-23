import json
import logging
from datetime import date

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LibraryController(http.Controller):

    @http.route('/api_ute/library/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_books(self, **kwargs):
        try:
            books = request.env['library.ute'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'author', 'headquarters', 'hous', 'gender', 'income'],
            )
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Libros obtenidos', 'data': books}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo libros')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/library/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_book(self, **kwargs):
        try:
            raw_data = request.httprequest.data
            if raw_data:
                body = json.loads(raw_data.decode('utf-8'))
            else:
                body = kwargs

            year_val = body.get('year') or body.get('income')
            if year_val and str(year_val).isdigit():
                income_date = f"{year_val}-01-01"
            else:
                income_date = str(date.today())

            vals = {
                'name': body.get('name'),
                'author': body.get('author'),
                'headquarters': body.get('headquarters', 'South'),
                'hous': body.get('hous', 'General'),
                'gender': body.get('gender', 'General'),
                'income': income_date,
            }

            record = request.env['library.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Libro creado exitosamente', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando libro en Odoo')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/library/delete/<int:book_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_book(self, book_id, **kwargs):
        try:
            record = request.env['library.ute'].sudo().browse(book_id)
            if not record.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Libro no encontrado'}),
                    status=404,
                    headers=[('Content-Type', 'application/json')]
                )
            record.unlink()
            return request.make_response(
                json.dumps({'status': 'success', 'message': f'Libro {book_id} eliminado'}),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error eliminando libro')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )