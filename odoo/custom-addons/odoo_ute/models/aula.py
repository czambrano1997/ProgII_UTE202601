from odoo import models, fields

class Aula(models.Model):
    _name = 'ou.aula'
    _description = 'Aulas de la UTE'
    _order = 'edificio, name'

    name = fields.Char(string='Nombre', required=True, tracking=True)
    edificio = fields.Char(string='Edificio', required=True, tracking=True)
    capacidad = fields.Integer(string='Capacidad', required=True, default=30, tracking=True)
    active = fields.Boolean(string='Activo', default=True)
