from odoo import models, fields


class Aula(models.Model):
    _name = 'ou.aula'
    _description = 'Aulas'

    name = fields.Char(string='Nombre', required=True)
    edificio = fields.Char(string='Edificio', required=True)
    capacidad = fields.Integer(string='Capacidad', required=True)
