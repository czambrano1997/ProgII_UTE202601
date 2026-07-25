from odoo import models, fields

class Carrera(models.Model):
    _name = 'ou.carrera'
    _description = 'Carreras de la UTE'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    codigo = fields.Char(string='Código', required=True, copy=False)
    modalidad = fields.Selection([
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('hibrida', 'Híbrida'),
    ], string='Modalidad', default='presencial', required=True, tracking=True)
    active = fields.Boolean(string='Activo', default=True)

    _sql_constraints = [
        ('unique_codigo_carrera', 'UNIQUE(codigo)', 'El código de la carrera debe ser único.'),
    ]
