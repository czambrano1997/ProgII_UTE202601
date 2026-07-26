from odoo import http
from odoo.http import request
import json

class ApiUte(http.Controller):
    @http.route('/api_ute/hello', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/api_ute/signature/all', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def list_signatures(self, **kw):
        signatures_data = request.env['ou.signature'].sudo().search_read([], ['id', 'name'])
        return request.make_response(
            json.dumps({'signatures': signatures_data}),
            headers=[('Content-Type', 'application/json')]
        )

    
    @http.route('/api_ute/signature/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_signatures(self, **kw):
        print("create_signatures")
        data = json.loads(request.httprequest.data)
        print(data)
        new_record = request.env['ou.signature'].sudo().create({
            'name': data['name']
        })
        return request.make_response(json.dumps({'status': 'success', 'new_record': new_record.id}), 
                                         headers=[('Content-Type', 'application/json')])