from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Rutas(models.Model):
    _name = 'ou.rutas'
    _description = 'Rutas de Transporte'
    _order = 'name'

    name = fields.Char(string='Nombre de la Ruta', required=True)
    distance_km = fields.Float(
        string='Distancia (km)',
        required=True,
        default=0.0,
        help='Distancia total de la ruta en kilómetros'
    )
    estimated_duration = fields.Float(
        string='Duración estimada (horas)',
        required=True,
        default=0.0,
        help='Tiempo estimado de recorrido en horas (ej: 1.5 = 1 hora 30 minutos)'
    )
    start_location = fields.Char(
        string='Punto de inicio',
        required=True,
        help='Dirección o punto de partida de la ruta'
    )
    end_location = fields.Char(
        string='Punto de llegada',
        required=True,
        help='Dirección o punto de destino de la ruta'
    )
    
    average_speed = fields.Float(
        string='Velocidad media (km/h)',
        compute='_compute_average_speed',
        store=True,
        help='Distancia / Duración estimada'
    )
    

    full_route = fields.Char(
        string='Ruta completa',
        compute='_compute_full_route',
        store=True,
    )


    @api.depends('distance_km', 'estimated_duration')
    def _compute_average_speed(self):
        """Calcula la velocidad media de la ruta."""
        for record in self:
            if record.estimated_duration > 0:
                record.average_speed = record.distance_km / record.estimated_duration
            else:
                record.average_speed = 0.0

    @api.depends('start_location', 'end_location')
    def _compute_full_route(self):
        """Genera una descripción completa de la ruta."""
        for record in self:
            record.full_route = f"{record.start_location} → {record.end_location}"

    @api.constrains('distance_km', 'estimated_duration')
    def _check_positive_values(self):
        """Valida que distancia y duración sean mayores a cero."""
        for record in self:
            if record.distance_km <= 0:
                raise ValidationError('La distancia debe ser mayor a 0 km.')
            if record.estimated_duration <= 0:
                raise ValidationError('La duración estimada debe ser mayor a 0 horas.')

    @api.onchange('start_location', 'end_location')
    def _onchange_locations(self):
        """Sugiere un nombre para la ruta si está vacío."""
        if not self.name and self.start_location and self.end_location:
            self.name = f"{self.start_location[:15]} → {self.end_location[:15]}"