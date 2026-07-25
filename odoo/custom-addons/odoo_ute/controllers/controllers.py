# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class ApiUte(http.Controller):

    @http.route('/api_ute/signature/all', type='http', auth='public', methods=['GET'], csrf=False)
    def signature_all(self, **kw):
        try:
            records = request.env['ou.signature'].sudo().search([])
            data = [{'id': r.id, 'name': r.name} for r in records]
            return request.make_response(json.dumps({'status': 'success', 'data': data}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/signature/create', type='http', auth='public', methods=['POST'], csrf=False)
    def signature_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            record = request.env['ou.signature'].sudo().create({'name': data.get('name')})
            return request.make_response(json.dumps({'status': 'success', 'message': 'Materia creada', 'id': record.id}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/signature/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def signature_delete(self, record_id, **kw):
        try:
            record = request.env['ou.signature'].sudo().browse(record_id)
            if record.exists():
                record.unlink()
                return request.make_response(json.dumps({'status': 'success', 'message': 'Materia eliminada'}), headers=[('Content-Type', 'application/json')])
            return request.make_response(json.dumps({'status': 'error', 'message': 'Registro no encontrado'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/teacher/all', type='http', auth='public', methods=['GET'], csrf=False)
    def teacher_all(self, **kw):
        try:
            records = request.env['sistema.usuarios'].sudo().search([])
            data = [{'id': r.id, 'name': r.name, 'last_name': r.last_name, 'email': r.email, 'phone': r.phone, 'vat': r.vat} for r in records]
            return request.make_response(json.dumps({'status': 'success', 'data': data}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/teacher/create', type='http', auth='public', methods=['POST'], csrf=False)
    def teacher_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            record = request.env['sistema.usuarios'].sudo().create({
                'name': data.get('name'), 'last_name': data.get('last_name'),
                'email': data.get('email'), 'phone': data.get('phone'), 'vat': data.get('vat')
            })
            return request.make_response(json.dumps({'status': 'success', 'message': 'Docente creado', 'id': record.id}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/teacher/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def teacher_delete(self, record_id, **kw):
        try:
            record = request.env['sistema.usuarios'].sudo().browse(record_id)
            if record.exists():
                record.unlink()
                return request.make_response(json.dumps({'status': 'success', 'message': 'Docente eliminado'}), headers=[('Content-Type', 'application/json')])
            return request.make_response(json.dumps({'status': 'error', 'message': 'Registro no encontrado'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/carrera/all', type='http', auth='public', methods=['GET'], csrf=False)
    def carrera_all(self, **kw):
        try:
            records = request.env['ou.carrera'].sudo().search([])
            data = [{'id': r.id, 'name': r.name, 'codigo': r.codigo, 'modalidad': r.modalidad} for r in records]
            return request.make_response(json.dumps({'status': 'success', 'data': data}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/carrera/create', type='http', auth='public', methods=['POST'], csrf=False)
    def carrera_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            record = request.env['ou.carrera'].sudo().create({
                'name': data.get('name'), 'codigo': data.get('codigo'), 'modalidad': data.get('modalidad')
            })
            return request.make_response(json.dumps({'status': 'success', 'message': 'Carrera creada', 'id': record.id}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/carrera/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def carrera_delete(self, record_id, **kw):
        try:
            record = request.env['ou.carrera'].sudo().browse(record_id)
            if record.exists():
                record.unlink()
                return request.make_response(json.dumps({'status': 'success', 'message': 'Carrera eliminada'}), headers=[('Content-Type', 'application/json')])
            return request.make_response(json.dumps({'status': 'error', 'message': 'Registro no encontrado'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/periodo/all', type='http', auth='public', methods=['GET'], csrf=False)
    def periodo_all(self, **kw):
        try:
            records = request.env['ou.periodo'].sudo().search([])
            data = [{'id': r.id, 'name': r.name, 'fecha_inicio': str(r.fecha_inicio) if r.fecha_inicio else None, 'fecha_fin': str(r.fecha_fin) if r.fecha_fin else None, 'activo': r.activo} for r in records]
            return request.make_response(json.dumps({'status': 'success', 'data': data}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/periodo/create', type='http', auth='public', methods=['POST'], csrf=False)
    def periodo_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            record = request.env['ou.periodo'].sudo().create({
                'name': data.get('name'), 'fecha_inicio': data.get('fecha_inicio'),
                'fecha_fin': data.get('fecha_fin'), 'activo': data.get('activo', True)
            })
            return request.make_response(json.dumps({'status': 'success', 'message': 'Período creado', 'id': record.id}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/periodo/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def periodo_delete(self, record_id, **kw):
        try:
            record = request.env['ou.periodo'].sudo().browse(record_id)
            if record.exists():
                record.unlink()
                return request.make_response(json.dumps({'status': 'success', 'message': 'Período eliminado'}), headers=[('Content-Type', 'application/json')])
            return request.make_response(json.dumps({'status': 'error', 'message': 'Registro no encontrado'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/aula/all', type='http', auth='public', methods=['GET'], csrf=False)
    def aula_all(self, **kw):
        try:
            records = request.env['ou.aula'].sudo().search([])
            data = [{'id': r.id, 'name': r.name, 'edificio': r.edificio, 'capacidad': r.capacidad} for r in records]
            return request.make_response(json.dumps({'status': 'success', 'data': data}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/aula/create', type='http', auth='public', methods=['POST'], csrf=False)
    def aula_create(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            record = request.env['ou.aula'].sudo().create({
                'name': data.get('name'), 'edificio': data.get('edificio'), 'capacidad': data.get('capacidad')
            })
            return request.make_response(json.dumps({'status': 'success', 'message': 'Aula creada', 'id': record.id}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])

    @http.route('/api_ute/aula/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def aula_delete(self, record_id, **kw):
        try:
            record = request.env['ou.aula'].sudo().browse(record_id)
            if record.exists():
                record.unlink()
                return request.make_response(json.dumps({'status': 'success', 'message': 'Aula eliminada'}), headers=[('Content-Type', 'application/json')])
            return request.make_response(json.dumps({'status': 'error', 'message': 'Registro no encontrado'}), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(json.dumps({'status': 'error', 'message': str(e)}), headers=[('Content-Type', 'application/json')])
