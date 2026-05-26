from odoo import models, fields

class Matricula(models.Model):
    _name = 'ute.matricula'
    _description = 'Matrícula'

    estudiante_id = fields.Many2one(
        'ute.estudiante',
        string="Estudiante"
    )

    fecha = fields.Date(string="Fecha")

    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('reprobado', 'Reprobado')
    ], string="Estado")

    aprobado = fields.Boolean(string="Aprobado")