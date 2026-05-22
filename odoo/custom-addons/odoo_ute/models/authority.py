from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Authority(models.Model):
    _name = 'ou.authority'
    _description = 'Autoridades y Coordinadores de la UTE'



    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Correo')
    phone = fields.Char(string='Teléfono')
    active = fields.Boolean(string='Activo', default=True)
    role = fields.Selection(
        selection=[
            ('coordinator', 'Coordinador de Carrera'),
            ('area_coordinator', 'Coordinador de Área'),
            ('director', 'Director de Carrera'),
            ('dean', 'Decano'),
            ('vice_dean', 'Subdecano'),],string='Cargo', required=True, default='coordinator')
    
    

    career_id = fields.Many2one(comodel_name='ou.career',string='Carrera a cargo')
    teacher_id = fields.Many2one(comodel_name='ou.teacher',string='Docente vinculado')
    start_date = fields.Date(string='Fecha de inicio del cargo')
    end_date = fields.Date(string='Fecha de fin del cargo')
    notes = fields.Text(string='Observaciones')
    full_name = fields.Char(string='Nombre Completo',compute='_compute_full_name',store=True)
    
    state = fields.Selection(
        selection=[
            ('active', 'En funciones'),
            ('inactive', 'Inactivo'),
            ('retired', 'Retirado'),
        ],string='Estado', default='active')



#@api.depends
    @api.depends('name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.name or ''} {rec.last_name or ''}".strip()

#@api.onchange
    @api.onchange('role')
    def onchange_role(self):
        if self.role == 'dean':
            return {
                'warning': {
                    'title': 'Cargo de alto nivel',
                    'message': 'El cargo de Decano requiere aprobación.'
                }
            }

    @api.onchange('teacher_id')
    def onchange_teacher(self):
        if self.teacher_id:
            self.name = self.teacher_id.name
            self.last_name = self.teacher_id.last_name
            self.email = self.teacher_id.email
            self.phone = self.teacher_id.phone

    #@api.constrai
    @api.constrains('start_date','end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError(
                    "La fecha de fin no puede ser antes de la de inicio.")
