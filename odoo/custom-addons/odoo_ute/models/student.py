from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date


class Student(models.Model):
    _name = 'ou.student'
    _description = 'Estudiantes de la UTE'


    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Correo institucional')
    phone = fields.Char(string='Teléfono')
    vat = fields.Char(string='CI/RUC', size=13)
    birth_date = fields.Date(string='Fecha de Nacimiento')
    age = fields.Integer(string='Edad', compute='_compute_age', store=True)
    active = fields.Boolean(string='Activo', default=True)


    gender = fields.Selection(selection=[('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')],string='Género')
    state = fields.Selection(
        selection=[
            ('enrolled', 'Matriculado'),
            ('graduated', 'Graduado'),
            ('withdrawn', 'Retirado'),
            ('suspended', 'Suspendido'),
        ],
        string='Estado', default='enrolled')
    

    enrollment_date = fields.Date(string='Fecha de Matrícula', default=fields.Date.today)
    gpa = fields.Float(string='Promedio General', digits=(4, 2))
    career_id = fields.Many2one(comodel_name='ou.career',string='Carrera',required=True)
    course_ids = fields.Many2many(comodel_name='ou.course',string='Cursos matriculados')
    notes = fields.Text(string='Observaciones')
    full_name = fields.Char(string='Nombre Completo',compute='_compute_full_name',store=True)
    is_honor_student = fields.Boolean(string='Estudiante de Honor',compute='_compute_honor',store=True)

#@api.depends
    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.name or ''} {rec.last_name or ''}".strip()
    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
    @api.depends('gpa')
    def _compute_honor(self):
        for rec in self:
            rec.is_honor_student = rec.gpa >= 9.0

# @api.onchang
    @api.onchange('career_id')
    def onchange_career(self):
        if self.career_id:
            return {
                'warning': {
                    'title': 'Carrera seleccionad',
                    'message': f'Se asignó la carrera: {self.career_id.name}'
                }
            }
    @api.onchange('gpa')
    def onchange_gpa(self):
        if self.gpa and (self.gpa < 0 or self.gpa > 10):
            return {
                'warning': {
                    'title': 'Promedio inválido',
                    'message': 'El promedio debe ser entre 0 y 10.'
                }
            }

    #@api.constrains
    @api.constrains('gpa')
    def _check_gpa(self):
        for rec in self:
            if rec.gpa < 0 or rec.gpa > 10:
                raise ValidationError("El promedio debe ser entre 0 y 10.")
    @api.constrains('vat')
    def _check_vat(self):
        for rec in self:
            if rec.vat and len(rec.vat) < 10:
                raise ValidationError("La CI debe tener al menos 10 caracteres.")
