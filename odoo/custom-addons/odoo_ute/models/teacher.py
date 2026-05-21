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
    validate_email = fields.Char(string="Validación", compute='_compute_validate_email',)
    signature_ids = fields.Many2many(comodel_name='ou.signature', string='Todas las materias')
    signature_primary = fields.Many2one(comodel_name='ou.signature', string='Materia principal')

    @api.onchange('vat')
    def onchange_vat(self):
        if self.vat and len(self.vat) < 10:
            raise ValidationError("La CI/RUC debe tener 10 o 13 caracteres")
    

    @api.depends('email')
    def _compute_validate_email(self):
        for rec in self:
            if rec.email and '@' in rec.email:
                rec.validate_email = 'Validado'
            else:
                rec.validate_email = 'No valido'

    @api.constrains('vat')
    def _check_vat(self):
        for rec in self:
            if rec.vat and len(rec.vat) < 10:
                raise ValidationError("La CI/RUC debe tener 10 o 13 caracteres")
    
    def generar_reporte(self):
        self.ensure_one()
        # Método de ejemplo para generar un reporte de docente
        return {
            'name': self.name,
            'email': self.email,
            'signature_primary': self.signature_primary.name if self.signature_primary else None,
        }