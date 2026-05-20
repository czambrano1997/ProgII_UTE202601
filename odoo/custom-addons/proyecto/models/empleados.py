# -*- coding: utf-8 -*-
from odoo import api,fields, models
from odoo.exceptions import ValidationError

class Empleados(models.Model):
    _name = 'concensionario.empleados'
    _description ='Tabla de Empleados '

    name = fields.Char(string='Nombre')
    cargo = fields.Selection(
        selection=[
            ('vendedor', 'Vendedor'),
            ('asesor', 'Asesor Comercial'),
            ('gerente_ventas', 'Gerente de Ventas'),
            ('mecanico', 'Mecánico'),
            ('administrador', 'Administrador'),
            ('recepcionista', 'Recepcionista'),
        ],
        string='Cargo',
        required=True,
        default='vendedor',
        tracking=True,
    )
    cedula = fields.Char(string='Cédula', size=10, required=True)
    email = fields.Char(string='Correo Corporativo')
    phone = fields.Char(string='Teléfono')
    tipo_contrato = fields.Selection(
        selection=[
            ('indefinido', 'Indefinido'),
            ('fijo', 'Plazo Fijo'),
            ('eventual', 'Eventual'),
        ],
        string='Tipo de Contrato',
        default='indefinido',
    )
    salary = fields.Float(string='Salario Base ($)', digits=(10, 2), required=True)
    comision_porcentaje = fields.Float(
        string='% Comisión por Venta', digits=(5, 2), default=2.0
    )
    comision_total = fields.Float(
        string='Total Comisiones ($)',
        compute='_compute_comision_total',
        store=True,
    )
    salario_total = fields.Float(
        string='Salario Total ($)',
        compute='_compute_salario_total',
        store=True,
    )
    fecha_ingreso = fields.Date(
        string='Fecha de Ingreso', required=True, default=fields.Date.today
    )
    fecha_salida = fields.Date(string='Fecha de Salida')
    anios_servicio = fields.Integer(
        string='Años de Servicio',
        compute='_compute_anios_servicio',
        store=True,
    )

    supervisor_id = fields.Many2one(
        'concesionario.empleado',
        string='Supervisor',
        domain="[('es_supervisor', '=', True)]",
    )
    subordinado_id = fields.One2many(
        'concesionario.empleado',
        'supervisor_id',
        string='Subordinados',
    )
    pedido_id = fields.One2many(
        'concesionario.pedido',
        'empleado_id',
        string='Ventas Realizadas',
    )
    cliente_id = fields.One2many(
        'concesionario.cliente',
        'empleado_asesor_id',
        string='Clientes Asignados',
    )

    @api.depends('pedido_id', 'pedido_id.total', 'comision_porcentaje')
    def _compute_comision_total(self):
        for rec in self:
            ventas = sum(
                p.total for p in rec.pedido_ids if p.estado == 'completado'
            )
            rec.comision_total = ventas * (rec.comision_porcentaje / 100)

    @api.depends('salary', 'comision_total')
    def _compute_salario_total(self):
        for rec in self:
            rec.salario_total = rec.salary + rec.comision_total

    @api.depends('fecha_ingreso')
    def _compute_anios_servicio(self):
        today = fields.Date.today()
        for rec in self:
            if rec.fecha_ingreso:
                delta = today - rec.fecha_ingreso
                rec.anios_servicio = int(delta.days / 365.25)
            else:
                rec.anios_servicio = 0

    @api.onchange('cargo')
    def _onchange_cargo(self):
        if self.cargo in ('gerente_ventas', 'administrador'):
            self.es_supervisor = True
        else:
            self.es_supervisor = False

    @api.onchange('estado')
    def _onchange_estado(self):
        if self.estado == 'inactivo':
            self.fecha_salida = fields.Date.today()
        else:
            self.fecha_salida = False

    @api.constrains('salary')
    def _check_salary(self):
        for rec in self:
            if rec.salary <= 0:
                raise ValidationError('El salario debe ser mayor a 0.')

    @api.constrains('comision_porcentaje')
    def _check_comision(self):
        for rec in self:
            if rec.comision_porcentaje < 0 or rec.comision_porcentaje > 100:
                raise ValidationError('El porcentaje de comisión debe estar entre 0 y 100.')

    @api.constrains('cedula')
    def _check_cedula(self):
        for rec in self:
            if rec.cedula and len(rec.cedula) != 10:
                raise ValidationError('La cédula del empleado debe tener 10 dígitos.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('codigo', 'Nuevo') == 'Nuevo':
                vals['codigo'] = self.env['ir.sequence'].next_by_code(
                    'concesionario.empleado'
                ) or 'EMP-0001'
        return super().create(vals_list)

    _sql_constraints = [
        ('cedula_unique', 'UNIQUE(cedula)', 'Ya existe un empleado con esa cédula.'),
    ]