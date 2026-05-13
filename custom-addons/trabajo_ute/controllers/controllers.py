# from odoo import http


# class TrabajoUte(http.Controller):
#     @http.route('/trabajo_ute/trabajo_ute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trabajo_ute/trabajo_ute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trabajo_ute.listing', {
#             'root': '/trabajo_ute/trabajo_ute',
#             'objects': http.request.env['trabajo_ute.trabajo_ute'].search([]),
#         })

#     @http.route('/trabajo_ute/trabajo_ute/objects/<model("trabajo_ute.trabajo_ute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trabajo_ute.object', {
#             'object': obj
#         })

