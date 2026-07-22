#from odoo import models, fields, api


# class api_ute(models.Model):
#     _name = 'api_ute.api_ute'
#     _description = 'api_ute.api_ute'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

