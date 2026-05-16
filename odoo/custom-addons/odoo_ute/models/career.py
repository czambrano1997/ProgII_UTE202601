# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Career(models.Model):
    _name = 'ou.career'
    _description = 'Carreras de la UTE'


    name = fields.Char(string='Nombre de Carrera', required=True)
    code = fields.Char(string='Código', size=10, required=True)
    duration_years = fields.Integer(string='Duración (años)', default=4)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activa', default=True)
    modality = fields.Selection(selection=[('presencial', 'Presencial'),('online', 'En línea'),('hybrid', 'Híbrida'),],string='Modalidad',default='presencial')
    coordinator_id = fields.Many2one(comodel_name='ou.teacher',string='Coordinador')
    signature_ids = fields.One2many(comodel_name='ou.signature',inverse_name='career_id',string='Materias')
    student_ids = fields.One2many(comodel_name='ou.student',inverse_name='career_id',string='Estudiantes')
    signature_count = fields.Integer(string='Nro. Materias',compute='_compute_signature_count',store=True)
    student_count = fields.Integer(string='Nro. Estudiantes',compute='_compute_student_count',store=True)


# @api.depends
    @api.depends('signature_ids')
    def _compute_signature_count(self):
        for rec in self:
            rec.signature_count = len(rec.signature_ids)
    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    #  @api.onchange
    @api.onchange('modality')
    def onchange_modality(self):
        if self.modality == 'online':
            return {
                'warning': {
                    'title': 'Información',
                    'message': 'La modalidad en línea debe tener configuración adicional.'
                }
            }



#@api.constrains
    @api.constrains('duration_years')
    def _check_duration(self):
        for rec in self:
            if rec.duration_years <= 0 or rec.duration_years > 10:
                raise ValidationError("La duración debe estar entre 1 y 10 años.")
    @api.constrains('code')
    def _check_code_unique(self):
        for rec in self:
            domain = [('code', '=', rec.code), ('id', '!=', rec.id)]
            if self.search(domain):
                raise ValidationError(f"El código de carrera '{rec.code}' ya existe.")
