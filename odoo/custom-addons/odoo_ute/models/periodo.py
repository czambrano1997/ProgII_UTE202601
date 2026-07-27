from odoo import models, fields

class Ute_periodo(models.Model):
    _name ='ou.periodo'
    _description = 'Periodo Académico'

    name = fields.Char(string = 'Nombre del periodo', required = True)
    fecha_inicio = fields.Date(string = 'fecha de inicio', required = True)
    fecha_fin = fields.Date(string = 'fecha de finalización', required=True)
    activo = fields.Boolean(string='Activo', default = True)
