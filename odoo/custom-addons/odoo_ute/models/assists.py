from odoo import models,fields,api

class assists(models.Model):
    _name = 'assists.ute'
    _description = 'assists.ute'

    student = fields.Many2one(
        string='Alumno',
        comodel_name='students.ute',
        required=True
    )
     
    signature = fields.Many2one(
        string='Asignatura',
        comodel_name='ou.signature',
        required=True
    )
    
    
    teachers = fields.Many2one(
        string='Profesores',
        comodel_name='ou.teacher',
        required=True
    )
    
    
    assists = fields.Selection(
        string='Asistencia',
        selection=[('assists', 'Asistio'), 
                    ('short', 'Falto'),
                    ('I_m_late','llego tarde'),
                    ('Justified','Falta justificada')
        ],
        required=True
    )
    
    attended =  fields.Boolean(
        string='Asistio',
        default='False',
        required=True
    )
    

