from odoo import models, fields, api


class Saleorder(models.Model):
    _inherit = 'sale.order'

    deliver_details = fields.Text(string="Detalles de entrega")
    
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
