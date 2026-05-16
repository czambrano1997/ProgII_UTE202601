# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError



class Producto(models.Model):
    _name = 'plasticos.producto'
    _description = 'Producto Plástico'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código', required=True)
    descripcion = fields.Text(string='Descripción')
    precio = fields.Float(string='Precio', digits=(10, 2))
    stock = fields.Integer(string='Stock', default=0)
    es_reciclable = fields.Boolean(string='Reciclable', default=True)
    fecha_creacion = fields.Date(string='Fecha', default=fields.Date.today)
    tipo_material = fields.Selection([
        ('pet', 'PET'), ('pe', 'PE'), ('pp', 'PP'),
        ('pvc', 'PVC'), ('ps', 'PS'), ('abs', 'ABS')
    ], string='Material', default='pet')
    estado = fields.Selection([
        ('activo', 'Activo'), ('descontinuado', 'Descontinuado')
    ], string='Estado', default='activo')

    categoria_id = fields.Many2one('plasticos.categoria', string='Categoría')
    venta_ids = fields.One2many('plasticos.venta.line', 'producto_id', string='Ventas')
    color_ids = fields.Many2many('plasticos.color', string='Colores')


    total_vendido = fields.Integer(string='Total Vendido', compute='_compute_total', store=True)


    @api.depends('venta_ids.cantidad')
    def _compute_total(self):
        for p in self:
            p.total_vendido = sum(v.cantidad for v in p.venta_ids)

    @api.constrains('precio')
    def _check_precio(self):
        for p in self:
            if p.precio <= 0:
                raise ValidationError('El precio debe ser mayor a 0')

    @api.constrains('stock')
    def _check_stock(self):
        for p in self:
            if p.stock < 0:
                raise ValidationError('El stock no puede ser negativo')

    @api.onchange('tipo_material')
    def _onchange_material(self):
        if self.tipo_material == 'pet':
            return {'warning': {'title': 'PET', 'message': 'Material 100% reciclable'}}

class Categoria(models.Model):
    _name = 'plasticos.categoria'
    _description = 'Categoría'
    name = fields.Char(string='Nombre', required=True)

class Color(models.Model):
    _name = 'plasticos.color'
    _description = 'Color'
    name = fields.Char(string='Nombre', required=True)
