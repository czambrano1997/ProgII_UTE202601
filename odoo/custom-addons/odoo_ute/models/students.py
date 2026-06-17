# Aqui se crea el modelo de lo estudiantes 
from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError



class students(models.Model):
    
    _name = 'students.ute'
    _description = 'students.ute'
    

    name = fields.Char(
        string='Nombres',
        required = True
    )

    surnames = fields.Char(
            string='Apellidos',
            required=True   
        )
        
    age = fields.Integer(
            string='Edad',
            required=True
        )
        
    phone = fields.Integer(
            string='telefono',
            required=True
        )
        
    vat = fields.Char(
            string="CI/RUC", 
            required=True,
            size=13
        )

    grade_ids = fields.One2many(
        comodel_name='grade.line',
        inverse_name='student_id',
        string='Notas'
        )


    @api.onchange('vat')
    def _onchange_vat(self):
        if self.vat and len(self.vat) < 10:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'La CI/RUC debe tener mínimo 10 o 13 caracteres'
                }
            }

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age and rec.age < 17:
                raise ValidationError("El estudiante debe ser mayor de 17 años")

    @api.depends('names', 'surnames')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.names or ''} {rec.surnames or ''}"

