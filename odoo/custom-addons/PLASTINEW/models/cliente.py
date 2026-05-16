# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Cliente(models.Model):
    _name = 'plasticos.cliente'
    _description = 'Cliente'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    rfc = fields.Char(string='RFC', required=True)
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    direccion = fields.Text(string='Dirección')
    tipo = fields.Selection([
        ('minorista', 'Minorista'), ('mayorista', 'Mayorista'), ('industrial', 'Industrial')
    ], string='Tipo', default='minorista')
    es_credito = fields.Boolean(string='Crédito', default=False)
    limite_credito = fields.Float(string='Límite', digits=(12, 2))
    estado = fields.Selection([
        ('activo', 'Activo'), ('inactivo', 'Inactivo')
    ], string='Estado', default='activo')

    venta_ids = fields.One2many('plasticos.venta', 'cliente_id', string='Ventas')
    total_compras = fields.Float(string='Total Compras', compute='_compute_compras', store=True)

    @api.depends('venta_ids.total')
    def _compute_compras(self):
        for c in self:
            c.total_compras = sum(v.total for v in c.venta_ids)

    @api.constrains('email')
    def _check_email(self):
        for c in self:
            if c.email and '@' not in c.email:
                raise ValidationError('Email inválido')

    @api.constrains('limite_credito', 'es_credito')
    def _check_credito(self):
        for c in self:
            if c.es_credito and c.limite_credito <= 0:
                raise ValidationError('El límite de crédito debe ser mayor a 0')

    @api.onchange('es_credito')
    def _onchange_credito(self):
        if not self.es_credito:
            self.limite_credito = 0
    