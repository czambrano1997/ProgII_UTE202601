from odoo import models, fields, api

class Horarios(models.Model):
    _name = 'odoo_ute.horarios'
    _description = 'Horario de curso'
    _rec_name = 'name'

    name = fields.Char(
        string='Descripción',
        compute='_compute_name',
        store=True
    )
    curso_id = fields.Many2one(
        'odoo_ute.cursos',
        string='Curso',
        required=True,
        ondelete='cascade'
    )
    dia_semana = fields.Selection(
        [
            ('lunes', 'Lunes'),
            ('martes', 'Martes'),
            ('miércoles', 'Miércoles'),
            ('jueves', 'Jueves'),
            ('viernes', 'Viernes'),
            ('sábado', 'Sábado'),
            ('domingo', 'Domingo'),
        ],
        string='Día de la semana',
        required=True
    )
    hora_inicio = fields.Float(
        string='Hora inicio',
        help="Formato: horas como flotante (ej: 8.5 = 08:30)",
        required=True
    )
    hora_fin = fields.Float(
        string='Hora fin',
        help="Formato: horas como flotante (ej: 10.0 = 10:00)",
        required=True
    )
    aula = fields.Char(string='Aula')

    @api.depends('curso_id', 'dia_semana', 'hora_inicio', 'hora_fin')
    def _compute_name(self):
        for record in self:
            curso = record.curso_id.nombre if record.curso_id else '?'
            dia = dict(self._fields['dia_semana'].selection).get(record.dia_semana, record.dia_semana)
            record.name = f"{curso} - {dia} {record.hora_inicio:.2f}-{record.hora_fin:.2f}" if record.hora_inicio and record.hora_fin else f"{curso} - {dia}"