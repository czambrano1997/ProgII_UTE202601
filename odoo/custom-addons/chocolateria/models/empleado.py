from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api

class Empleado(models.Model):
    _name = 'choco.empleado'
    _description = 'Empleados'

    nombre = fields.Char(string='Nombre')
    cargo = fields.Char(string='Cargo')
    salario = fields.Float(string='Salario')
    activo = fields.Boolean(string='Activo', default=True)

    @api.constrains('salario')
    def _check_salario(self):
        for record in self:
            if record.salario <= 0:
                raise ValidationError(
                    "El salario debe ser mayor a cero"
                )