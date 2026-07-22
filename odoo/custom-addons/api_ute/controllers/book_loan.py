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
                json.dumps({'status': 'success', 'message': 'Préstamos obtenidos', 'data': loans}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error obteniendo préstamos')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api_ute/book_loan/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_book_loan(self, **kwargs):
        try:
            body = json.loads(request.httprequest.data)
            vals = {
                'name': int(body.get('student_id')) if body.get('student_id') else False,
                'book': int(body.get('book_id')) if body.get('book_id') else False,
                'loan_date': body.get('loan_date'),
                'book_observations': body.get('book_observations'),
            }
            record = request.env['book_loan.ute'].sudo().create(vals)
            return request.make_response(
                json.dumps({'status': 'success', 'message': 'Préstamo creado', 'id': record.id}, default=str),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception('Error creando préstamo')
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}, default=str),
                status=500, headers=[('Content-Type', 'application/json')]
            )