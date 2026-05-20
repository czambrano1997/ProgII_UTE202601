# from odoo import http


# class Trabajo(http.Controller):
#     @http.route('/trabajo/trabajo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trabajo/trabajo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('trabajo.listing', {
#             'root': '/trabajo/trabajo',
#             'objects': http.request.env['trabajo.trabajo'].search([]),
#         })

#     @http.route('/trabajo/trabajo/objects/<model("trabajo.trabajo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trabajo.object', {
#             'object': obj
#         })

