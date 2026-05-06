# from odoo import http


# class UteModulo(http.Controller):
#     @http.route('/ute_modulo/ute_modulo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ute_modulo/ute_modulo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ute_modulo.listing', {
#             'root': '/ute_modulo/ute_modulo',
#             'objects': http.request.env['ute_modulo.ute_modulo'].search([]),
#         })

#     @http.route('/ute_modulo/ute_modulo/objects/<model("ute_modulo.ute_modulo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ute_modulo.object', {
#             'object': obj
#         })

