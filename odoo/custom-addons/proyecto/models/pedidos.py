# -*- coding: utf-8 -*-
from odoo import api,fields, models
from odoo.exceptions import ValidationError

class Pedidos(models.Model):
    _name = 'concensionario.pedidos'
    _description = 'Tabla de Pedidos'

    name = fields.Char(
        string='Número de Pedido',
        readonly=True,
        default='Nuevo',
        copy=False,
        tracking=True,
    )
    fecha_pedido = fields.Date(
        string='Fecha del Pedido',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    fecha_entrega = fields.Date(string='Fecha de Entrega Estimada')
    fecha_entrega_real = fields.Date(string='Fecha de Entrega Real')
    estado = fields.Selection(
        selection=[
            ('borrador', 'Borrador'),
            ('confirmado', 'Confirmado'),
            ('en_proceso', 'En Proceso'),
            ('completado', 'Completado'),
            ('cancelado', 'Cancelado'),
        ],
        string='Estado',
        default='borrador',
        required=True,
        tracking=True,
    )
    tipo_pago = fields.Selection(
        selection=[
            ('contado', 'Contado'),
            ('credito', 'Crédito'),
            ('financiamiento', 'Financiamiento'),
            ('permuta', 'Permuta'),
        ],
        string='Tipo de Pago',
        default='contado',
        required=True,
    )
    cliente_id = fields.Many2one(
        'concesionario.cliente',
        string='Cliente',
        required=True,
        tracking=True,
        ondelete='restrict',
    )
    vehiculo_id = fields.Many2one(
        'concesionario.vehiculo',
        string='Vehículo',
        required=True,
        domain="[('estado', '=', 'disponible')]",
        tracking=True,
        ondelete='restrict',
    )
    empleado_id = fields.Many2one(
        'concesionario.empleado',
        string='Vendedor',
        required=True,
        domain="[('cargo', 'in', ['vendedor', 'asesor', 'gerente_ventas'])]",
    )
    precio_vehiculo = fields.Float(
        string='Precio Vehículo ($)',
        digits=(12, 2),
        compute='_compute_precio_vehiculo',
        store=True,
        readonly=False,
    )
    total = fields.Float(
        string='Total ($)',
        digits=(12, 2),
        compute='_compute_total',
        store=True,
        tracking=True,
    )
    meses_financiamiento = fields.Integer(
        string='Meses Financiamiento',
        default=0,
    )
    cuota_mensual = fields.Float(
        string='Cuota Mensual ($)',
        compute='_compute_cuota_mensual',
        store=True,
    )

    # ── Campos booleanos ────────────────────────────────────────────
    incluye_accesorios = fields.Boolean(string='Incluye Accesorios')
    entrega_a_domicilio = fields.Boolean(string='Entrega a Domicilio')

    # ── Campos texto ────────────────────────────────────────────────
    observaciones = fields.Text(string='Observaciones')
    condiciones_pago = fields.Html(string='Condiciones de Pago')

    # ── Compute ─────────────────────────────────────────────────────
    @api.depends('vehiculo_id')
    def _compute_precio_vehiculo(self):
        for rec in self:
            if rec.vehiculo_id:
                rec.precio_vehiculo = rec.vehiculo_id.precio_venta
            else:
                rec.precio_vehiculo = 0.0

    @api.depends('precio_vehiculo', 'descuento')
    def _compute_descuento_monto(self):
        for rec in self:
            rec.descuento_monto = rec.precio_vehiculo * (rec.descuento / 100)

    @api.depends('precio_vehiculo', 'descuento_monto')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.precio_vehiculo - rec.descuento_monto

    @api.depends('total', 'meses_financiamiento', 'tipo_pago')
    def _compute_cuota_mensual(self):
        for rec in self:
            if rec.tipo_pago == 'financiamiento' and rec.meses_financiamiento > 0:
                rec.cuota_mensual = rec.total / rec.meses_financiamiento
            else:
                rec.cuota_mensual = 0.0

    # ── Onchange ────────────────────────────────────────────────────
    @api.onchange('tipo_pago')
    def _onchange_tipo_pago(self):
        if self.tipo_pago != 'financiamiento':
            self.meses_financiamiento = 0

    @api.onchange('vehiculo_id')
    def _onchange_vehiculo(self):
        if self.vehiculo_id:
            self.precio_vehiculo = self.vehiculo_id.precio_venta

    @api.onchange('cliente_id')
    def _onchange_cliente(self):
        if self.cliente_id and self.cliente_id.empleado_asesor_id:
            self.empleado_id = self.cliente_id.empleado_asesor_id

    # ── Constrains ──────────────────────────────────────────────────
    @api.constrains('descuento')
    def _check_descuento(self):
        for rec in self:
            if rec.descuento < 0 or rec.descuento > 100:
                raise ValidationError('El descuento debe estar entre 0% y 100%.')

    @api.constrains('fecha_entrega', 'fecha_pedido')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_entrega and rec.fecha_entrega < rec.fecha_pedido:
                raise ValidationError(
                    'La fecha de entrega no puede ser anterior a la fecha del pedido.'
                )

    @api.constrains('meses_financiamiento')
    def _check_meses(self):
        for rec in self:
            if rec.tipo_pago == 'financiamiento' and rec.meses_financiamiento <= 0:
                raise ValidationError(
                    'Debe indicar los meses de financiamiento (mayor a 0).'
                )

    # ── Acciones ────────────────────────────────────────────────────
    def action_confirmar(self):
        for rec in self:
            rec.estado = 'confirmado'
            rec.vehiculo_id.estado = 'reservado'

    def action_completar(self):
        for rec in self:
            rec.estado = 'completado'
            rec.vehiculo_id.estado = 'vendido'
            rec.vehiculo_id.fecha_venta = fields.Date.today()

    def action_cancelar(self):
        for rec in self:
            if rec.estado in ('confirmado', 'en_proceso'):
                rec.vehiculo_id.estado = 'disponible'
            rec.estado = 'cancelado'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'concesionario.pedido'
                ) or 'PED-0001'
        return super().create(vals_list)