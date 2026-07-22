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

            # Construimos la fecha 'YYYY-MM-DD' usando el Year si viene de Django
            year_val = body.get('year') or body.get('income')
            if year_val and str(year_val).isdigit():
                income_date = f"{year_val}-01-01"
            else:
                income_date = str(date.today())

            # Mapeamos los campos completando los que faltan con valores por defecto
            vals = {
                'name': body.get('name'),
                'author': body.get('author'),
                'headquarters': body.get('headquarters', 'South'),  # Por defecto 'South'
                'hous': body.get('hous', 'General'),              # Por defecto 'General'
                'gender': body.get('gender', 'General'),          # Por defecto 'General'
                'income': income_date,                            # Fecha válida ISO
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