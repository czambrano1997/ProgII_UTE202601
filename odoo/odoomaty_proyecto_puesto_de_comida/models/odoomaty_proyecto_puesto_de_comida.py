# -*- coding: utf-8 -*-
from odoo import api,fields,models

class FoodOrder(models.Model):
    _name = 'food.order'
    _description = 'Pedido del Puesto de Comida'
    _order = 'id desc'

    name = fields.Char(string='Número de Pedido', required=True, copy=False, readonly=True, index=True, default=lambda self: 'Nuevo')
    customer_name = fields.Char(string='Nombre del Cliente', required=True, default='Anónimo')
    order_date = fields.Datetime(string='Fecha del Pedido', default=fields.Datetime.now, readonly=True)
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('cooking', 'En Cocina'),
        ('ready', 'Listo para Entrega'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)
    
    order_line_ids = fields.One2many('food.order.line', 'order_id', string='Líneas de Pedido')
    amount_total = fields.Float(string='Total a Pagar', compute='_compute_amount_total', store=True)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.order_line_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                # Genera un código simple para el puesto de comida (ej. ORD-001)
                vals['name'] = self.env['ir.sequence'].next_by_code('food.order') or 'Nuevo'
        return super(FoodOrder, self).create(vals_list)

    def action_kitchen(self):
        self.write({'state': 'cooking'})

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_deliver(self):
        self.write({'state': 'delivered'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})


class FoodOrderLine(models.Model):
    _name = 'food.order.line'
    _description = 'Línea de Pedido de Comida'

    order_id = fields.Many2one('food.order', string='Pedido', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Platillo/Bebida', required=True, domain=[('sale_ok', '=', True)])
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    price_unit = fields.Float(string='Precio Unitario', related='product_id.list_price', readonly=False)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
    notes = fields.Char(string='Notas (Sin cebolla, extra queso, etc.)')

    @api.depends('quantity', 'price_unit')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit