from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Signature(models.Model):
    _name = 'ou.signature'
    _description = 'Materias de la UTE'

    name = fields.Char(string='Materia', required=True)
    code = fields.Char(string='Código', size=10)
    credits = fields.Integer(string='Créditos', default=3)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activa', default=True)
    
    
    
    level = fields.Selection(
        selection=[
            ('1', 'Primer nivel'), ('2', 'Segundo nivel'),
            ('3', 'Tercer nivel'), ('4', 'Cuarto nivel'),
            ('5', 'Quinto nivel'), ('6', 'Sexto nivel'),
            ('7', 'Séptimo nivel'), ('8', 'Octavo nivel'),
        ],string='Nivel')
    

    career_id = fields.Many2one(comodel_name='ou.career',string='Carrera')
    teacher_ids = fields.Many2many(comodel_name='ou.teacher',string='Docentes')
    course_count = fields.Integer(string='Nro. Cursos',compute='_compute_course_count',store=True)
    course_ids = fields.One2many(comodel_name='ou.course',inverse_name='signature_id',string='Cursos')

# @api.depends
    @api.depends('course_ids')
    def _compute_course_count(self):
        for rec in self:
            rec.course_count = len(rec.course_ids)

    #@api.onchange
    @api.onchange('credits')
    def onchange_credits(self):
        if self.credits and self.credits > 10:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'El número de créditos es muy alto.'
                }
            }

# @api.constrains
    @api.constrains('credits')
    def _check_credits(self):
        for rec in self:
            if rec.credits <= 0:
                raise ValidationError("Los créditos deben ser numeros positivos.")
    @api.constrains('code')
    def _check_code_unique(self):
        for rec in self:
            if rec.code:
                domain = [('code', '=', rec.code), ('id', '!=', rec.id)]
                if self.search(domain):
                    raise ValidationError(f"El código '{rec.code}' ya existe con otra materia.")
