# from odoo import models, fields, api


# class trabajo_ute(models.Model):
#     _name = 'trabajo_ute.trabajo_ute'
#     _description = 'trabajo_ute.trabajo_ute'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

