import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BookLoanController(http.Controller):

    @http.route('/api_ute/book_loan/all', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_book_loans(self, **kwargs):
        try:
            loans = request.env['book_loan.ute'].sudo().search_read(
                domain=[],
                fields=['id', 'name', 'book', 'book_gender', 'loan_date', 'book_observations'],
            )
            return request.make_response(
                # Agregado default=str para serializar loan_date y campos Many2one
                json.dumps({'status': 'success', 'message': 'Prestamos obtenidos', 'data': loans}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo prestamos')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/book_loan/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_book_loan(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data)
            
            # Aseguramos conversion de IDs si son campos Many2one
            student_id = int(body.get('student_id')) if body.get('student_id') else False
            book_id = int(body.get('book_id')) if body.get('book_id') else False

            vals = {
                'name': student_id or body.get('student_id'),
                'book': book_id or body.get('book_id'),
                'loan_date': body.get('loan_date'),
                'book_observations': body.get('book_observations'),
            }
            record = request.env['book_loan.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Prestamo creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando prestamo')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/book_loan/delete/<int:loan_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_book_loan(self, loan_id, **kwargs):
        try:
            record = request.env['book_loan.ute'].sudo().browse(loan_id)
            if not record.exists():
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'Prestamo no encontrado'}, default=str),
                    status=404,
                    headers=[('Content-Type', 'application/json')]
                )
            record.unlink()
            return request.make_response(
                json.dumps({'status': 'success', 'message': f'Prestamo {loan_id} eliminado'}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error eliminando prestamo')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500,
                headers=[('Content-Type', 'application/json')]
            )