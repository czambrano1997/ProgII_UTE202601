# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PatitasUnidasHogarAdoptivo(models.Model):
    _name = 'patitas.unidas.hogar_adoptivo'
    _description = 'Hogar Adoptivo / Temporal'
    _rec_name = 'name'
    _order = 'name asc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre del Cuidador', required=True, index=True, tracking=True)
    address = fields.Text(string='Dirección')
    max_capacity = fields.Integer(string='Capacidad Máxima', default=1)
    active = fields.Boolean(string='Activo', default=True, tracking=True)

    pets_ids = fields.One2many('patitas.unidas.mascota', 'foster_home_id', string='Mascotas Alojadas')

    current_occupancy = fields.Integer(
        string='Ocupación Actual', compute='_compute_occupancy_metrics', store=True, index=True
    )
    occupancy_percentage = fields.Float(
        string='% Ocupación', compute='_compute_occupancy_metrics', store=True
    )
    available_slots = fields.Integer(
        string='Plazas Libres', compute='_compute_occupancy_metrics', store=True
    )

    @api.depends('pets_ids', 'max_capacity')
    def _compute_occupancy_metrics(self):
        for record in self:
            occupied = len(record.pets_ids)
            record.current_occupancy = occupied
            record.available_slots = max(0, record.max_capacity - occupied)
            record.occupancy_percentage = (occupied / record.max_capacity * 100) if record.max_capacity > 0 else 0.0

    @api.constrains('max_capacity')
    def _check_max_capacity(self):
        for record in self:
            if record.max_capacity < 1:
                raise ValidationError(_('La capacidad máxima debe ser al menos 1.'))
