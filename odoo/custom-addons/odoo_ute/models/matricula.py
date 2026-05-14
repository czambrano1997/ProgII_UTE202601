from odoo import models, fields, api

class Matricula(models.Model):
    _name = 'odoo_ute.matricula'
    _description = 'Matrícula'
    _rec_name = 'name'

    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
    )
    alumno_id = fields.Many2one(
        'odoo_ute.alumno',
        string='Alumno',
        required=True,
        ondelete='cascade'
    )
    curso_id = fields.Many2one(
        'odoo_ute.cursos',
        string='Curso',
        required=True,
        ondelete='cascade'
    )
    fecha_matricula = fields.Date(
        string='Fecha de matrícula',
        default=fields.Date.today
    )
    nota_final = fields.Float(
        string='Nota final',
        digits=(3, 2),  # Permite hasta 9.99, ajusta según necesites
        help="Nota en escala de 0 a 10 (o la que uses)"
    )

    @api.depends('alumno_id', 'curso_id')
    def _compute_name(self):
        for record in self:
            alumno = record.alumno_id.name if record.alumno_id else '?'
            curso = record.curso_id.nombre if record.curso_id else '?'
            record.name = f"{alumno} - {curso}"