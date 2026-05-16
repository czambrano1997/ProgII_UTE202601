# from odoo import http


# class PatitasUnidas(http.Controller):
#     @http.route('/patitas_unidas/patitas_unidas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/patitas_unidas/patitas_unidas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('patitas_unidas.listing', {
#             'root': '/patitas_unidas/patitas_unidas',
#             'objects': http.request.env['patitas_unidas.patitas_unidas'].search([]),
#         })

#     @http.route('/patitas_unidas/patitas_unidas/objects/<model("patitas_unidas.patitas_unidas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('patitas_unidas.object', {
#             'object': obj
#         })

