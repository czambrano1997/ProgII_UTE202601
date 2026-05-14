from odoo import models,fields,api

class assists(models.Model):
    _name = 'assists.ute'
    _description = 'assists.ute'

    student = fields.Many2one(
        string='Alumno',
        comodel_name='students.ute',
    )
     
    signature = fields.Many2one(
        string='Asignatura',
        comodel_name='ou.signature',
    )
    
    
    teachers = fields.Many2one(
        string='Profesores',
        comodel_name='ou.teacher',
    )
    
    
    assists = fields.Selection(
        string='Asistencia',
        selection=[('assists', 'Asistio'), 
                    ('short', 'Falto'),
                    ('I_m_late','llego tarde'),
                    ('Justified','Falta justificada')
        ]
    )
        

