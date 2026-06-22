# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TeatroFuncion(models.Model):
    _name = 'teatro.funcion'
    _description = 'Función de teatro'
    _order = 'fecha desc, hora_inicio'

    obra_id = fields.Many2one(
        comodel_name='teatro.obra',
        string='Obra',
        required=True,
    )
    fecha = fields.Date(
        string='Fecha',
        required=True,
        default=fields.Date.context_today,
    )
    hora_inicio = fields.Float(
        string='Hora de inicio',
        digits=(6, 2),
        required=True,
        default=20.0,
    )
    lugar = fields.Char(
        string='Sala / Lugar',
        required=True,
        default='Sala Principal',
    )
    capacidad = fields.Integer(
        string='Capacidad',
        default=100,
        required=True,
    )
    boletos_ids = fields.One2many(
        comodel_name='teatro.boleto',
        inverse_name='funcion_id',
        string='Boletos',
    )
    asientos_vendidos = fields.Integer(
        string='Boletos vendidos',
        compute='_compute_asientos',
        store=True,
    )
    asientos_disponibles = fields.Integer(
        string='Asientos disponibles',
        compute='_compute_asientos',
        store=True,
    )
    state = fields.Selection(
        [
            ('borrador', 'Borrador'),
            ('confirmada', 'Confirmada'),
            ('cerrada', 'Cerrada'),
        ],
        string='Estado',
        default='borrador',
        required=True,
    )

    @api.depends('boletos_ids')
    def _compute_asientos(self):
        for rec in self:
            rec.asientos_vendidos = len(rec.boletos_ids)
            rec.asientos_disponibles = max(0, rec.capacidad - rec.asientos_vendidos)

    @api.constrains('capacidad', 'boletos_ids')
    def _check_capacidad(self):
        for rec in self:
            if rec.capacidad < 0:
                raise ValidationError('La capacidad debe ser un número positivo.')
            if len(rec.boletos_ids) > rec.capacidad:
                raise ValidationError('No se puede vender más boletos que la capacidad de la función.')
