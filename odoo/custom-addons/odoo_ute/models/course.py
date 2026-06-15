from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'ou.course'
    _description = 'Cursos de la UTE'


    name = fields.Char(string='Nombre del Curso', required=True)
    code = fields.Char(string='Código', size=15)
    signature_id = fields.Many2one(comodel_name='ou.signature',string='Materia',required=True)
    teacher_id = fields.Many2one(comodel_name='ou.teacher',string='Docente')
    student_ids = fields.Many2many(comodel_name='ou.student',string='Estudiantes')
    period = fields.Char(string='Periodo acadeemico', help='Ej: 2025-A')
    start_date = fields.Date(string='Fecha de inicio')
    end_date = fields.Date(string='Fecha de fin')
    capacity = fields.Integer(string='Capacidad máxima', default=30)
    enrolled_count = fields.Integer(string='Estudiantes matriculados',compute='_compute_enrolled_count',store=True)
    available_spots = fields.Integer(string='Cupos disponibles',compute='_compute_available_spots',store=True)
    
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('open', 'Abierto'),
            ('in_progress', 'En Curso'),
            ('finished', 'Finalizado'),
            ('cancelled', 'Cancelado'),],string='Estado', default='draft')
    schedule = fields.Text(string='Horario')
    classroom = fields.Char(string='Aula')
    notes = fields.Html(string='Notas del curso')


    @api.depends('student_ids')
    def _compute_enrolled_count(self):
        for rec in self:
            rec.enrolled_count = len(rec.student_ids)

    @api.depends('capacity', 'enrolled_count')
    def _compute_available_spots(self):
        for rec in self:
            rec.available_spots = max(0, rec.capacity - rec.enrolled_count)


#@api.onchange
    @api.onchange('signature_id')
    def onchange_signature(self):
        if self.signature_id and self.signature_id.teacher_ids:
            self.teacher_id = self.signature_id.teacher_ids[0]

    @api.onchange('start_date', 'end_date')
    def onchange_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            return {
                'warning': {
                    'title': 'Fechas inválidas',
                    'message': 'La fecha de fin no puede ser antees a la de inicio.'
                }
            }


    #@api.constrains
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError("Fecha de fin no puede ser antes a la de inicio.")

    @api.constrains('capacity')
    def _check_capacity(self):
        for rec in self:
            if rec.capacity <= 0:
                raise ValidationError("Capacidad máxima debe ser mayor a 0.")



    #cambiar estado del cursoo
    def action_open(self):
        self.state = 'open'

    def action_start(self):
        self.state = 'in_progress'

    def action_finish(self):
        self.state = 'finished'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'