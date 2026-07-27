import json
from odoo import http
from odoo.http import request


class ApiUte(http.Controller):

    @http.route('/api_ute/hello', auth='public')
    def index(self, **kw):
        return "Hello, world"


    def _json_response(self, data, status=200):
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')],
            status=status
        )

    # 1.signature
   
    @http.route('/api_ute/signature/all', type='http', auth='public', methods=['GET'], csrf=False)
    def list_signatures(self, **kw):
        records = request.env['ou.signature'].sudo().search_read([], ['id', 'name'])
        return self._json_response({'status': 'success', 'data': records})

    @http.route('/api_ute/signature/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_signatures(self, **kw):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body) if raw_body else {}
            new_record = request.env['ou.signature'].sudo().create({
                'name': data.get('name')
            })
            return self._json_response({'status': 'success', 'message': 'Materia creada', 'id': new_record.id})
        except Exception as e:
            return self._json_response({'status': 'error', 'message': str(e)}, status=400)

    @http.route('/api_ute/signature/delete/<int:rec_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_signature(self, rec_id, **kw):
        rec = request.env['ou.signature'].sudo().browse(rec_id)
        if rec.exists():
            rec.unlink()
            return self._json_response({'status': 'success', 'message': 'Materia eliminada'})
        return self._json_response({'status': 'error', 'message': 'Registro no encontrado'}, status=404)

    # 2. usuarios
   
    @http.route('/api_ute/usuarios/all', type='http', auth='public', methods=['GET'], csrf=False)
    def list_usuarios(self, **kw):
        records = request.env['sistema.usuarios'].sudo().search_read(
            [], ['id', 'name', 'last_name', 'email', 'phone', 'vat']
        )
        return self._json_response({'status': 'success', 'data': records})

    @http.route('/api_ute/usuarios/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_usuario(self, **kw):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body) if raw_body else {}
            new_record = request.env['sistema.usuarios'].sudo().create({
                'name': data.get('name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'vat': data.get('vat')
            })
            return self._json_response({'status': 'success', 'message': 'Docente creado', 'id': new_record.id})
        except Exception as e:
            return self._json_response({'status': 'error', 'message': str(e)}, status=400)

    @http.route('/api_ute/usuarios/delete/<int:rec_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_usuario(self, rec_id, **kw):
        rec = request.env['sistema.usuarios'].sudo().browse(rec_id)
        if rec.exists():
            rec.unlink()
            return self._json_response({'status': 'success', 'message': 'Docente eliminado'})
        return self._json_response({'status': 'error', 'message': 'Registro no encontrado'}, status=404)

    # 3.carrera
    @http.route('/api_ute/carrera/all', type='http', auth='public', methods=['GET'], csrf=False)
    def list_carreras(self, **kw):
        records = request.env['ou.carrera'].sudo().search_read([], ['id', 'name', 'codigo', 'modalidad'])
        return self._json_response({'status': 'success', 'data': records})

    @http.route('/api_ute/carrera/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_carrera(self, **kw):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body) if raw_body else {}
            new_record = request.env['ou.carrera'].sudo().create({
                'name': data.get('name'),
                'codigo': data.get('codigo'),
                'modalidad': data.get('modalidad', 'presencial')
            })
            return self._json_response({'status': 'success', 'message': 'Carrera creada', 'id': new_record.id})
        except Exception as e:
            return self._json_response({'status': 'error', 'message': str(e)}, status=400)

    @http.route('/api_ute/carrera/delete/<int:rec_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_carrera(self, rec_id, **kw):
        rec = request.env['ou.carrera'].sudo().browse(rec_id)
        if rec.exists():
            rec.unlink()
            return self._json_response({'status': 'success', 'message': 'Carrera eliminada'})
        return self._json_response({'status': 'error', 'message': 'Registro no encontrado'}, status=404)

    # 4.periodo
    @http.route('/api_ute/periodo/all', type='http', auth='public', methods=['GET'], csrf=False)
    def list_periodos(self, **kw):
        records = request.env['ou.periodo'].sudo().search([])
        data = [{
            'id': r.id,
            'name': r.name or '',
            'fecha_inicio': str(r.fecha_inicio) if r.fecha_inicio else '',
            'fecha_fin': str(r.fecha_fin) if r.fecha_fin else '',
            'activo': r.activo
        } for r in records]
        return self._json_response({'status': 'success', 'data': data})

    @http.route('/api_ute/periodo/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_periodo(self, **kw):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body) if raw_body else {}
            new_record = request.env['ou.periodo'].sudo().create({
                'name': data.get('name'),
                'fecha_inicio': data.get('fecha_inicio'),
                'fecha_fin': data.get('fecha_fin'),
                'activo': data.get('activo', True)
            })
            return self._json_response({'status': 'success', 'message': 'Periodo creado', 'id': new_record.id})
        except Exception as e:
            return self._json_response({'status': 'error', 'message': str(e)}, status=400)

    @http.route('/api_ute/periodo/delete/<int:rec_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_periodo(self, rec_id, **kw):
        rec = request.env['ou.periodo'].sudo().browse(rec_id)
        if rec.exists():
            rec.unlink()
            return self._json_response({'status': 'success', 'message': 'Periodo eliminado'})
        return self._json_response({'status': 'error', 'message': 'Registro no encontrado'}, status=404)

    
    # 5.aula
    
    @http.route('/api_ute/aula/all', type='http', auth='public', methods=['GET'], csrf=False)
    def list_aulas(self, **kw):
        records = request.env['ou.aula'].sudo().search_read([], ['id', 'name', 'edificio', 'capacidad'])
        return self._json_response({'status': 'success', 'data': records})

    @http.route('/api_ute/aula/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_aula(self, **kw):
        try:
            raw_body = request.httprequest.data
            data = json.loads(raw_body) if raw_body else {}
            new_record = request.env['ou.aula'].sudo().create({
                'name': data.get('name'),
                'edificio': data.get('edificio'),
                'capacidad': data.get('capacidad', 30)
            })
            return self._json_response({'status': 'success', 'message': 'Aula creada', 'id': new_record.id})
        except Exception as e:
            return self._json_response({'status': 'error', 'message': str(e)}, status=400)

    @http.route('/api_ute/aula/delete/<int:rec_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_aula(self, rec_id, **kw):
        rec = request.env['ou.aula'].sudo().browse(rec_id)
        if rec.exists():
            rec.unlink()
            return self._json_response({'status': 'success', 'message': 'Aula eliminada'})
        return self._json_response({'status': 'error', 'message': 'Registro no encontrado'}, status=404)