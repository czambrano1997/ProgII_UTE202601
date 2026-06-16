from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Horario(models.Model):
    _name = 'ou.horario'
    _description = 'Horario de Operación'
    _order = 'day_of_week, start_time'

    name = fields.Char(string='Nombre del Horario', required=True)
    day_of_week = fields.Selection(
        selection=[
            ('monday', 'Lunes'),
            ('tuesday', 'Martes'),
            ('wednesday', 'Miércoles'),
            ('thursday', 'Jueves'),
            ('friday', 'Viernes'),
            ('saturday', 'Sábado'),
            ('sunday', 'Domingo'),
        ],
        string='Día de la semana',
        required=True,
        default='monday',
        help='Día al que aplica este horario'
    )
    start_time = fields.Float(
        string='Hora de inicio',
        required=True,
        default=8.0,
        help='Hora de inicio en formato decimal (ej: 8.0 = 08:00, 8.5 = 08:30)'
    )
    end_time = fields.Float(
        string='Hora de fin',
        required=True,
        default=17.0,
        help='Hora de finalización en formato decimal'
    )
    is_active = fields.Boolean(
        string='Activo',
        default=True,
        help='Indica si el horario está disponible para asignación'
    )
    
    duration_hours = fields.Float(
        string='Duración (horas)',
        compute='_compute_duration',
        store=True,
        help='Diferencia entre hora de fin y hora de inicio'
    )

    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Calcula la duración total del horario."""
        for record in self:
            record.duration_hours = record.end_time - record.start_time

    @api.constrains('start_time', 'end_time')
    def _check_time_range(self):
        """Valida que la hora de fin sea posterior a la hora de inicio."""
        for record in self:
            if record.end_time <= record.start_time:
                raise ValidationError('La hora de fin debe ser mayor que la hora de inicio.')

    @api.onchange('start_time', 'end_time')
    def _onchange_time_range(self):
        """Genera un nombre sugerido automáticamente si el campo name está vacío."""
        if not self.name and self.start_time and self.end_time:
            day_label = dict(self._fields['day_of_week'].selection).get(self.day_of_week, '')
            self.name = f"{day_label} {self.start_time:.1f}-{self.end_time:.1f}"