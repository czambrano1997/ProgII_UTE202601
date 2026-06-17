# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError

class Producto(models.Model):
    _name = 'concensionario.producto'
    _description = 'Tabla de Productos'
    name = fields.Char(string='Nombre del Producto')
    codigo = fields.Char(
        string='Código',
        readonly=True,
        default='Nuevo',
        copy=False,
    )
    referencia = fields.Char(string='Referencia Interna')
    categoria = fields.Selection(
        selection=[
            ('accesorio', 'Accesorio'),
            ('repuesto', 'Repuesto'),
            ('lubricante', 'Lubricante'),
            ('electronico', 'Electrónico'),
            ('seguridad', 'Seguridad'),
            ('limpieza', 'Limpieza'),
        ],
        string='Categoría',
        required=True,
        default='accesorio',
    )
    unidad_medida = fields.Selection(
        selection=[
            ('unidad', 'Unidad'),
            ('par', 'Par'),
            ('kit', 'Kit'),
            ('litro', 'Litro'),
            ('metro', 'Metro'),
        ],
        string='Unidad de Medida',
        default='unidad',
    )
    estado = fields.Selection(
        selection=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
            ('agotado', 'Agotado'),
        ],
        string='Estado',
        default='activo',
        tracking=True,
    )
    price = fields.Float(string='Precio de Venta ($)', digits=(10, 2), required=True)
    costo = fields.Float(string='Costo ($)', digits=(10, 2))
    stock = fields.Integer(string='Stock Actual', default=0)
    stock_minimo = fields.Integer(string='Stock Mínimo', default=5)

    disponible = fields.Boolean(
        string='Disponible',
        compute='_compute_disponible',
        store=True,
    )
    alerta_stock = fields.Boolean(
        string='Alerta de Stock Bajo',
        compute='_compute_alerta_stock',
        store=True,
    )
    es_original = fields.Boolean(string='Pieza Original', default=True)

    proveedor_id = fields.Many2one(
        'concesionario.proveedor',
        string='Proveedor',
        ondelete='set null',
    )
    vehiculo_ids = fields.Many2many(
        'concesionario.vehiculo',
        'vehiculo_producto_rel',
        'producto_id',
        'vehiculo_id',
        string='Vehículos Compatibles',
    )

    descripcion = fields.Text(string='Descripción')
    notas = fields.Html(string='Notas Técnicas')

    @api.depends('stock', 'estado')
    def _compute_disponible(self):
        for rec in self:
            rec.disponible = rec.stock > 0 and rec.estado == 'activo'

    @api.depends('stock', 'stock_minimo')
    def _compute_alerta_stock(self):
        for rec in self:
            rec.alerta_stock = rec.stock <= rec.stock_minimo

    @api.onchange('stock')
    def _onchange_stock(self):
        if self.stock == 0:
            self.estado = 'agotado'
        elif self.estado == 'agotado' and self.stock > 0:
            self.estado = 'activo'

    @api.onchange('costo')
    def _onchange_costo(self):
        """Sugerir precio de venta con 30% de margen."""
        if self.costo and self.costo > 0 and not self.price:
            self.price = self.costo * 1.30

    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price <= 0:
                raise ValidationError('El precio de venta debe ser mayor a 0.')

    @api.constrains('stock', 'stock_minimo')
    def _check_stock(self):
        for rec in self:
            if rec.stock < 0:
                raise ValidationError('El stock no puede ser negativo.')
            if rec.stock_minimo < 0:
                raise ValidationError('El stock mínimo no puede ser negativo.')
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'concesionario.producto'
                ) or 'PROD-0001'
        return super().create(vals_list)