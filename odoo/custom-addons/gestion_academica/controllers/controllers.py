# -*- coding: utf-8 -*-
# from odoo import http


# class GestionAcademica(http.Controller):
#     @http.route('/gestion_academica/gestion_academica', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_academica/gestion_academica/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_academica.listing', {
#             'root': '/gestion_academica/gestion_academica',
#             'objects': http.request.env['gestion_academica.gestion_academica'].search([]),
#         })

#     @http.route('/gestion_academica/gestion_academica/objects/<model("gestion_academica.gestion_academica"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_academica.object', {
#             'object': obj
#         })

