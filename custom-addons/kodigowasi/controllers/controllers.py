# from odoo import http


# class Kodigowasi(http.Controller):
#     @http.route('/kodigowasi/kodigowasi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kodigowasi/kodigowasi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kodigowasi.listing', {
#             'root': '/kodigowasi/kodigowasi',
#             'objects': http.request.env['kodigowasi.kodigowasi'].search([]),
#         })

#     @http.route('/kodigowasi/kodigowasi/objects/<model("kodigowasi.kodigowasi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kodigowasi.object', {
#             'object': obj
#         })

