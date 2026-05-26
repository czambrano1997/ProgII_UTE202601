from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Empleado(models.Model):
    _name = 'choco.empleado'
    _description = 'Empleados'

    # Se cambia 'nombre' a 'name' para que Odoo lo reconozca automáticamente
    name = fields.Char(string='Nombre', required=True)
    puesto = fields.Char(string='Puesto')
    salario = fields.Float(string='Salario')
    activo = fields.Boolean(string='Activo', default=True)

    @api.constrains('salario')
    def _check_salario(self):
        for record in self:
            if record.salario <= 0:
                raise ValidationError(
                    "El salario debe ser mayor a cero"
                )