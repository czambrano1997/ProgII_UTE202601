# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError

class Vehiculos(models.Model):
    _name = 'concensionario.vehiculo'
    _description = 'Tabla de Vechiculos'

    placa = fields.Char(string='Placa')
    year = fields.Integer(string='Año', required=True)
    color = fields.Char(string='Color')
    price= fields.Float(
        string='Precio de Venta', digits=(12, 2), required=True, tracking=True
    )
    kilometraje = fields.Integer(string='Kilometraje (km)', default=0)
    cilindraje = fields.Float(string='Cilindraje (cc)', digits=(6, 1))
    tipo_vehiculo = fields.Selection(
        selection=[
            ('sedan', 'Sedán'),
            ('suv', 'SUV'),
            ('pickup', 'Pickup'),
            ('furgoneta', 'Furgoneta'),
            ('camion', 'Camión'),
            ('moto', 'Motocicleta'),
        ],
        string='Tipo de Vehículo',
        required=True,
        default='sedan',
    )
    combustible = fields.Selection(
        selection=[
            ('gasolina', 'Gasolina'),
            ('diesel', 'Diésel'),
            ('hibrido', 'Híbrido'),
            ('electrico', 'Eléctrico'),
        ],
        string='Combustible',
        default='gasolina',
    )
    estado = fields.Selection(
        selection=[
            ('disponible', 'Disponible'),
            ('reservado', 'Reservado'),
            ('vendido', 'Vendido'),
            ('mantenimiento', 'En Mantenimiento'),
        ],
        string='Estado',
        default='disponible',
        tracking=True,
    )
    condicion = fields.Selection(
        selection=[('nuevo', 'Nuevo'), ('usado', 'Usado')],
        string='Condición',
        default='nuevo',
        required=True,
    )
    proveedor_id = fields.Many2one(
        'concesionario.proveedor',
        string='Proveedor',
        ondelete='set null',
    )
    empleado_vendedor_id = fields.Many2one(
        'concesionario.empleado',
        string='Vendedor Asignado',
    )
    producto_id = fields.Many2many(
        'concesionario.producto',
        'vehiculo_producto_rel',
        'vehiculo_id',
        'producto_id',
        string='Accesorios / Productos',
    )
    pedido_id = fields.One2many(
        'concesionario.pedido',
        'vehiculo_id',
        string='Pedidos',
    )
    descripcion = fields.Text(string='Descripción Detallada')
    notas_internas = fields.Html(string='Notas Internas')

    margen_ganancia = fields.Float(
        string='Margen de Ganancia (%)',
        compute='_compute_margen_ganancia',
        store=True,
    )
    total_accesorios = fields.Float(
        string='Total Accesorios',
        compute='_compute_total_accesorios',
        store=True,
    )
    precio_total = fields.Float(
        string='Precio Total (con accesorios)',
        compute='_compute_precio_total',
        store=True,
    )
    cantidad_pedidos = fields.Integer(
        string='Nº Pedidos',
        compute='_compute_cantidad_pedidos',
    )

    @api.depends('precio_venta', 'precio_costo')
    def _compute_margen_ganancia(self):
        for rec in self:
            if rec.precio_costo and rec.precio_costo > 0:
                rec.margen_ganancia = (
                    (rec.precio_venta - rec.precio_costo) / rec.precio_costo
                ) * 100
            else:
                rec.margen_ganancia = 0.0

    @api.depends('producto_id', 'producto_id.price')
    def _compute_total_accesorios(self):
        for rec in self:
            rec.total_accesorios = sum(rec.producto_ids.mapped('price'))

    @api.depends('precio_venta', 'total_accesorios')
    def _compute_precio_total(self):
        for rec in self:
            rec.precio_total = rec.precio_venta + rec.total_accesorios

    def _compute_cantidad_pedidos(self):
        for rec in self:
            rec.cantidad_pedidos = len(rec.pedido_ids)

    @api.onchange('condicion')
    def _onchange_condicion(self):
        """Al cambiar a usado se desmarca garantía por defecto."""
        if self.condicion == 'usado':
            self.tiene_garantia = False
        else:
            self.tiene_garantia = True

    @api.onchange('tipo_vehiculo')
    def _onchange_tipo_vehiculo(self):
        """Sugerencia de combustible según tipo."""
        if self.tipo_vehiculo == 'electrico':
            self.combustible = 'electrico'
        elif self.tipo_vehiculo in ('camion', 'pickup'):
            self.combustible = 'diesel'

    @api.constrains('precio_venta', 'precio_costo')
    def _check_precios(self):
        for rec in self:
            if rec.precio_venta <= 0:
                raise ValidationError('El precio de venta debe ser mayor a 0.')
            if rec.precio_costo and rec.precio_venta < rec.precio_costo:
                raise ValidationError(
                    'El precio de venta no puede ser menor al costo.'
                )

    @api.constrains('year')
    def _check_anio(self):
        for rec in self:
            if rec.anio < 1900 or rec.year > 2100:
                raise ValidationError('El año del vehículo no es válido.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'concesionario.vehiculo'
                ) or 'VEH-0001'
        return super().create(vals_list)