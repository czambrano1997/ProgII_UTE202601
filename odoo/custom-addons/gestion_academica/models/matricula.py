from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestionMatricula(models.Model):
    _name = 'gestion.matricula'
    _description = 'Matrícula'

    name = fields.Char(string='Código de matrícula', required=True)

    estudiante_id = fields.Many2one(
        'gestion.estudiante',
        string='Estudiante',
        required=True
    )

    curso_id = fields.Many2one(
        'gestion.curso',
        string='Curso',
        required=True
    )

    fecha_matricula = fields.Date(
        string='Fecha de matrícula',
        default=fields.Date.today
    )

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado', default='borrador')

    costo = fields.Float(string='Costo')
    descuento = fields.Float(string='Descuento')

    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True
    )

    materia_ids = fields.Many2many(
        'gestion.materia',
        string='Materias'
    )

    @api.depends('costo', 'descuento')
    def _compute_total(self):
        for record in self:
            record.total = record.costo - record.descuento

    @api.onchange('curso_id')
    def _onchange_curso_id(self):
        if self.curso_id:
            self.materia_ids = self.curso_id.materia_ids

    @api.constrains('descuento', 'costo')
    def _check_descuento(self):
        for record in self:
            if record.descuento > record.costo:
                raise ValidationError('El descuento no puede ser mayor que el costo.')