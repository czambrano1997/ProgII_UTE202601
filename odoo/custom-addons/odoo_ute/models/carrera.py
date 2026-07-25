from odoo import models, fields


class Carrera(models.Model):
    _name = 'ou.carrera'
    _description = 'Carreras'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    modalidad = fields.Selection(
        [('presencial', 'Presencial'), ('virtual', 'Virtual'), ('mixto', 'Mixto')],
        string='Modalidad',
        required=True,
    )
