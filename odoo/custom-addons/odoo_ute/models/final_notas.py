from odoo import models,fields,api

class final_notes(models.Model):

    _name = 'final_notes.ute'
    _description = 'final_notes.ute'

    
    name = fields.Many2one(
        string='Estudiante',
        comodel_name='students.ute',
        required=True
    )

    teacher = fields.Many2one(
        string='Docente',
        comodel_name='ou.teacher',
        required=True
    )
    
    
    teacher_signature = fields.Char(
        string='Materia',
        required=True
    )
    