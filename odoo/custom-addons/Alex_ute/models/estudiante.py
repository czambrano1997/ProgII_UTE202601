from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Estudiante(models.Model):
    _name = 'ute.estudiante'
    _description = 'Estudiante UTE'

    name = fields.Char(string='Nombre', required=True)
    cedula = fields.Char(string='Cédula', size=10)
    edad = fields.Integer(string='Edad')
    carrera_id = fields.Many2one(
        string='Carrera',
        comodel_name='ute.carrera',
    )

    @api.constrains('edad')
    def _check_edad(self):
        for record in self:
            if record.edad < 0:
                raise ValidationError("La edad no puede ser negativa")