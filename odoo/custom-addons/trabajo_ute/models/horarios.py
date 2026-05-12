from odoo import fields, models

class horario(models.Model):
    _name = 'ou.horario'

    name = fields.Char(string='Horario')
