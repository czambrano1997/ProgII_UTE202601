from odoo import models, fields

class Periodo(models.Model):
    _name = 'ou.periodo'
    _description = 'Períodos Académicos'
    _order = 'fecha_inicio desc'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True, tracking=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True, tracking=True)
    activo = fields.Boolean(string='Activo', default=True, tracking=True)

    _sql_constraints = [
        ('unique_periodo_name', 'UNIQUE(name)', 'El nombre del período debe ser único.'),
    ]
