# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Inventario(models.Model):
    _name = 'plasticos.inventario'
    _description = 'Inventario'
    _order = 'fecha desc'

    name = fields.Char(string='Referencia', readonly=True, default='Nuevo')
    producto_id = fields.Many2one('plasticos.producto', string='Producto', required=True)
    tipo = fields.Selection([
        ('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste', 'Ajuste')
    ], string='Tipo', default='entrada')
    cantidad = fields.Float(string='Cantidad', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    ubicacion = fields.Char(string='Ubicación')
    motivo = fields.Text(string='Motivo')
    estado = fields.Selection([
        ('borrador', 'Borrador'), ('confirmado', 'Confirmado')
    ], string='Estado', default='borrador')

    stock_anterior = fields.Float(string='Stock Anterior', readonly=True)
    stock_nuevo = fields.Float(string='Stock Nuevo', compute='_compute_stock', store=True)

    @api.depends('stock_anterior', 'cantidad', 'tipo')
    def _compute_stock(self):
        for i in self:
            if i.tipo == 'entrada':
                i.stock_nuevo = i.stock_anterior + i.cantidad
            elif i.tipo == 'salida':
                i.stock_nuevo = i.stock_anterior - i.cantidad
            else:
                i.stock_nuevo = i.cantidad

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for i in self:
            if i.cantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor a 0')

    @api.constrains('stock_anterior', 'cantidad', 'tipo')
    def _check_stock(self):
        for i in self:
            if i.tipo == 'salida' and i.stock_anterior < i.cantidad:
                raise ValidationError('Stock insuficiente para la salida')

    @api.onchange('tipo')
    def _onchange_tipo(self):
        if self.tipo == 'salida':
            return {'warning': {'title': 'Salida', 'message': 'Verifique stock disponible'}}

    def action_confirmar(self):
        self.write({'estado': 'confirmado'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('plasticos.inventario') or 'INV001'
        return super(Inventario, self).create(vals)
