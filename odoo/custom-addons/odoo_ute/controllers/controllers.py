# from odoo import http


# class OdooUte(http.Controller):
#     @http.route('/odoo_ute/odoo_ute', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_ute/odoo_ute/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_ute.listing', {
#             'root': '/odoo_ute/odoo_ute',
#             'objects': http.request.env['odoo_ute.odoo_ute'].search([]),
#         })

#     @http.route('/odoo_ute/odoo_ute/objects/<model("odoo_ute.odoo_ute"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_ute.object', {
#             'object': obj
#         })

