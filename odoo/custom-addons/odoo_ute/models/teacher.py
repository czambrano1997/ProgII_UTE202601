from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TeacherUTE(models.Model):
    _name = 'ou.teacher'
    _description = 'Docentes de la UTE'

    name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido", required=True)
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Teléfono")
    vat = fields.Char(string="CI/RUC", size=13)
    # subject_ids = fields.One2many('ou.subject.teacher', 'teacher_id')

    @api.onchange('vat')
    def onchange_vat(self):
        if self.vat and len(self.vat) < 10:
            raise ValidationError("La CI/RUC debe tener 10 o 13 caracteres")
    