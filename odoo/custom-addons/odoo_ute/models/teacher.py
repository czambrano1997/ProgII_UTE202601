from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TeacherUTE(models.Model):
    _name = 'ou.teacher'
    _description = 'Docentes de la UTE'

    name = fields.Char(string="Apodo", required=True)
    last_name = fields.Char(string="Apellido", required=True)
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Teléfono")
    vat = fields.Char(string="CI/RUC", size=13)
    active = fields.Boolean(string="Activo", default=True)
    birth_date = fields.Date(string="Fecha de Nacimiento")
    salary = fields.Float(string="Salario", digits=(10, 2))
    notes = fields.Text(string="Observaciones")



    gender = fields.Selection(selection=[('male', 'Masculino'), ('female', 'Femenino'),('other', 'Otro')],string="Género")
    state = fields.Selection(selection=[('active', 'Activo'), ('inactive', 'Inactivo'),('retired', 'Jubilado')],string="Estado", default='active')
    validate_email = fields.Char(string="Validación Email",compute='_compute_validate_email',store=True)
    full_name = fields.Char(string="Nombre Completo",compute='_compute_full_name',store=True)
    signature_ids = fields.Many2many(comodel_name='ou.signature',string='Materias que dá')
    signature_primary = fields.Many2one(comodel_name='ou.signature',string='Materia Principal')
    course_ids = fields.One2many(comodel_name='ou.course',inverse_name='teacher_id',string='Cursos asignados')



#@api.depends
    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.name or ''} {rec.last_name or ''}".strip()
    @api.depends('email')
    def _compute_validate_email(self):
        for rec in self:
            if rec.email and '@' in rec.email:
                rec.validate_email = 'Validado'
            else:
                rec.validate_email = 'No válido'

# @api.onchange
    @api.onchange('vat')
    def onchange_vat(self):
        if self.vat and len(self.vat) < 10:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'La CI/RUC debe tener al menos 10 caracteres.'
                }
            }
    @api.onchange('signature_primary')
    def onchange_signature_primary(self):
        if self.signature_primary and self.signature_primary not in self.signature_ids:
            self.signature_ids = [(4, self.signature_primary.id)]


#@api.constrains
    @api.constrains('vat')
    def _check_vat(self):
        for rec in self:
            if rec.vat and len(rec.vat) < 10:
                raise ValidationError("La CI/RUC debe tener 10 o 13 caracteres.")
    @api.constrains('salary')
    def _check_salary(self):
        for rec in self:
            if rec.salary < 0:
                raise ValidationError("El salario no puede ser negativo.")
    def generar_reporte(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Reporte',
                'message': f'Reporte generado para {self.full_name}',
                'type': 'success',
            }
        }