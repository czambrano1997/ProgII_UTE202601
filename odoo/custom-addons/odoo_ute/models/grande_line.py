from odoo import models,fields,api

class GradeLine(models.Model):
    _name = 'grade.line'
    _description = 'Nota por materia'

    student_id = fields.Many2one(
        comodel_name='students.ute',
        string='Estudiante'
    )

    signature_id = fields.Many2one(
        comodel_name='ou.signature',
        string='Materia'
    )

    grade = fields.Float(
        string='Nota',
    )