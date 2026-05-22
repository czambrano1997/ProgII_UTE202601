from odoo import models, fields

class Carrera(models.Model):
    _name = 'ute.carrera'
    _description = 'Carrera'

    name = fields.Char(string="Nombre", required=True)
    facultad = fields.Char(string="Facultad")
    duracion = fields.Integer(string="Duración")
    activa = fields.Boolean(string="Activa", default=True)

    estudiante_ids = fields.One2many(
        'ute.estudiante',
        'carrera_id',
        string="Estudiantes"
    )