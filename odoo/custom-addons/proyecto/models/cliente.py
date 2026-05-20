# -*- coding: utf-8 -*-
from odoo import api,fields, models
from odoo.exceptions import ValidationError


class Cliente(models.Model):
    _name = 'concensionario.cliente'
    _description = 'Tabla de Clientes'

    name = fields.Char(string='Nombre')
    vat = fields.Char(string="CI/RUC", size=13)
    email = fields.Char(string="Correo")
    phone = fields.Char(string="Teléfono")
    direction = fields.Char(string="Dirección")
    validate_email = fields.Char(string="Validación", compute='_compute_validate_email',)
    birth_date = fields.Date(string='Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute= '_compute_edad')
    


cliente_id = fields.Many2one(
    'empresa.cliente',
    string='Cliente')
pedido_ids = fields.One2many(
    'concesionario.pedido',
    'cliente_id',
    string='Pedidos',
    )
empleado_asesor_id = fields.Many2one(
    'concesionario.empleado',
    string='Asesor Asignado',
    )

total_compras = fields.Float(
    string='Total Compras ($)',
    compute='_compute_total_compras',
    store=True,
    )

@api.depends('fecha_nacimiento')
def _compute_edad(self):
    today = fields.Date.today()
    for rec in self:
        if rec.fecha_nacimiento:
            elta = today - rec.fecha_nacimiento
            rec.edad = int(delta.days / 365.25)
        else:
            rec.edad = 0

    @api.depends('email')
    def _compute_validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        for rec in self:
            rec.validate_email = bool(rec.email and re.match(pattern, rec.email))

    @api.depends('pedido_id', 'pedido_id.total')
    def _compute_total_compras(self):
        for rec in self:
            rec.total_compras = sum(
                p.total for p in rec.pedido_ids if p.estado == 'completado'
            )

    def _compute_cantidad_pedidos(self):
        for rec in self:
            rec.cantidad_pedidos = len(rec.pedido_ids)


    @api.onchange('tipo_identificacion')
    def _onchange_tipo_identificacion(self):
        self.vat = False

    @api.constrains('vat', 'tipo_identificacion')
    def _check_vat(self):
        for rec in self:
            if not rec.vat:
                continue
            if rec.tipo_identificacion == 'cedula' and len(rec.vat) != 10:
                raise ValidationError('La cédula debe tener 10 dígitos.')
            if rec.tipo_identificacion == 'ruc' and len(rec.vat) != 13:
                raise ValidationError('El RUC debe tener 13 dígitos.')

    @api.constrains('credito_aprobado')
    def _check_credito(self):
        for rec in self:
            if rec.credito_aprobado < 0:
                raise ValidationError('El crédito aprobado no puede ser negativo.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'concesionario.cliente'
                ) or 'CLI-0001'
        return super().create(vals_list)

    _sql_constraints = [
        ('vat_unique', 'UNIQUE(vat)', 'Ya existe un cliente con esa identificación.'),
    ]