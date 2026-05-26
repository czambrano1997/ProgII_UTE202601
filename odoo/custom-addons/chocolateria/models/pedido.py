from odoo import models, fields, api

class Pedido(models.Model):
    _name = 'choco.pedido'
    _description = 'Pedidos'

    name = fields.Char(string='Referencia de Pedido', required=True, default='Nuevo')

    cliente_id = fields.Many2one('choco.cliente', string='Cliente')
    fecha = fields.Date(string='Fecha')
    
    empleado_id = fields.Many2one('hr.employee', string='Empleado')
    
    detalle_ids = fields.One2many(
        'choco.detalle',
        'pedido_id',
        string='Detalles'
    )

    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True
    )

    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado')
    ], default='borrador')

    @api.depends('detalle_ids.subtotal')
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(
                detalle.subtotal for detalle in pedido.detalle_ids
            )