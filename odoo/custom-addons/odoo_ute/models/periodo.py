from odoo import models, fields


class Periodo(models.Model):
    _name = 'ou.periodo'
    _description = 'Periodos'

    name = fields.Char(string='Nombre', required=True)
    fecha_inicio = fields.Date(string='Fecha inicio', required=True)
    fecha_fin = fields.Date(string='Fecha fin', required=True)
    activo = fields.Boolean(string='Activo', default=True)
