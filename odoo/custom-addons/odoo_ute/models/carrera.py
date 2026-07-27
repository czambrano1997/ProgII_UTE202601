from odoo import models, fields


class Ute_carrera(models.Model):
    _name = 'ou.carrera'
    _description = 'Carrera Universitaria'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código')
    modalidad = fields.Selection([
        ('presencial','Presencial'),
        ('semipresencial','Semipresencial'),
        ('en_linea','Enn linea'),
    ], string='Modalidad', default='presencial', required=True)
