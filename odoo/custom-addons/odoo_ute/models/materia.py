from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestionMateria(models.Model):
    _name = 'gestion.materia'
    _description = 'Materia'

    name = fields.Char(string='Nombre de la materia', required=True)
    codigo = fields.Char(string='Código', required=True)
    creditos = fields.Integer(string='Créditos')
    horas = fields.Float(string='Horas semanales')

    profesor_id = fields.Many2one(
        'gestion.profesor',
        string='Profesor',
        required=True
    )

    curso_id = fields.Many2one(
        'gestion.curso',
        string='Curso',
        required=True
    )

    profesor_email = fields.Char(
        string='Correo del profesor',
        related='profesor_id.email',
        store=True
    )

    @api.onchange('creditos')
    def _onchange_creditos(self):
        if self.creditos:
            self.horas = self.creditos * 2

    @api.constrains('creditos')
    def _check_creditos(self):
        for record in self:
            if record.creditos and record.creditos <= 0:
                raise ValidationError('Los créditos deben ser mayores que cero.')