# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Venta(models.Model):
    _name = 'plasticos.venta'
    _description = 'Venta'
    _order = 'fecha desc'

    name = fields.Char(string='Folio', readonly=True, default='Nuevo')
    cliente_id = fields.Many2one('plasticos.cliente', string='Cliente', required=True)
    fecha = fields.Date(string='Fecha', default=fields.Date.today)
    metodo_pago = fields.Selection([
        ('efectivo', 'Efectivo'), ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'), ('credito', 'Crédito')
    ], string='Pago', default='efectivo')
    estado = fields.Selection([
        ('borrador', 'Borrador'), ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='borrador')
    notas = fields.Text(string='Notas')

    line_ids = fields.One2many('plasticos.venta.line', 'venta_id', string='Líneas')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    impuestos = fields.Float(string='Impuestos (16%)', compute='_compute_impuestos', store=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('line_ids.subtotal')
    def _compute_subtotal(self):
        for v in self:
            v.subtotal = sum(l.subtotal for l in v.line_ids)

    @api.depends('subtotal')
    def _compute_impuestos(self):
        for v in self:
            v.impuestos = v.subtotal * 0.16

    @api.depends('subtotal', 'impuestos')
    def _compute_total(self):
        for v in self:
            v.total = v.subtotal + v.impuestos

    @api.constrains('line_ids')
    def _check_lineas(self):
        for v in self:
            if v.estado != 'borrador' and not v.line_ids:
                raise ValidationError('La venta necesita al menos un producto')

    @api.onchange('cliente_id')
    def _onchange_cliente(self):
        if self.cliente_id and self.cliente_id.es_credito:
            self.metodo_pago = 'credito'

    def action_confirmar(self):
        for v in self:
            if not v.line_ids:
                raise ValidationError('Agregue productos primero')
            v.write({'estado': 'confirmada'})

    def action_cancelar(self):
        self.write({'estado': 'cancelada'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('plasticos.venta') or 'VTA001'
        return super(Venta, self).create(vals)

class VentaLine(models.Model):
    _name = 'plasticos.venta.line'
    _description = 'Línea de Venta'

    venta_id = fields.Many2one('plasticos.venta', string='Venta', required=True, ondelete='cascade')
    producto_id = fields.Many2one('plasticos.producto', string='Producto', required=True)
    cantidad = fields.Float(string='Cantidad', default=1)
    precio_unitario = fields.Float(string='Precio', digits=(10, 2))
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for l in self:
            l.subtotal = l.cantidad * l.precio_unitario

    @api.constrains('cantidad')
    def _check_cantidad(self):
        for l in self:
            if l.cantidad <= 0:
                raise ValidationError('La cantidad debe ser mayor a 0')

    @api.onchange('producto_id')
    def _onchange_producto(self):
        if self.producto_id:
            self.precio_unitario = self.producto_id.precio
