# from odoo import http


# class Odoo-ute(http.Controller):
#     @http.route('/odoo-ute/odoo-ute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-ute/odoo-ute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-ute.listing', {
#             'root': '/odoo-ute/odoo-ute',
#             'objects': http.request.env['odoo-ute.odoo-ute'].search([]),
#         })

#     @http.route('/odoo-ute/odoo-ute/objects/<model("odoo-ute.odoo-ute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-ute.object', {
#             'object': obj
#         })

