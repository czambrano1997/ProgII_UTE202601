# -*- coding: utf-8 -*-
# from odoo import http


# class BibliotecaUte(http.Controller):
#     @http.route('/biblioteca_ute/biblioteca_ute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/biblioteca_ute/biblioteca_ute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('biblioteca_ute.listing', {
#             'root': '/biblioteca_ute/biblioteca_ute',
#             'objects': http.request.env['biblioteca_ute.biblioteca_ute'].search([]),
#         })

#     @http.route('/biblioteca_ute/biblioteca_ute/objects/<model("biblioteca_ute.biblioteca_ute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biblioteca_ute.object', {
#             'object': obj
#         })
