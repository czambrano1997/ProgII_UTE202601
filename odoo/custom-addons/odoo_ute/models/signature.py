from odoo import fields, models

class Signature(models.Model):
    _name = 'ou.signature'
    name = fields.Char(string='Materia')