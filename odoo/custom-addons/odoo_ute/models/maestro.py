# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Maestro(models.Model):
    _name = 'odoo_ute_v2.maestro'
    _description = 'Maestro'
    _rec_name = 'name'
    _order = 'apellido, nombre'

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True,
        index=True,
    )
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Email', index=True)
    especialidad = fields.Char(string='Especialidad')
    active = fields.Boolean(string='Activo', default=True)

    curso_ids = fields.One2many(
        'odoo_ute_v2.cursos', 'maestro_id', string='Cursos impartidos'
    )
    num_cursos = fields.Integer(
        string='N° de cursos',
        compute='_compute_num_cursos',
        store=True,
    )

    @api.depends('nombre', 'apellido')
    def _compute_name(self):
        for r in self:
            partes = [p for p in [r.apellido, r.nombre] if p]
            r.name = ', '.join(partes) if partes else _('Sin nombre')

    @api.depends('curso_ids')
    def _compute_num_cursos(self):
        for r in self:
            r.num_cursos = len(r.curso_ids)

    @api.constrains('email')
    def _validar_email(self):
        for r in self:
            if r.email and '@' not in r.email:
                raise ValidationError(_('El correo electrónico no tiene un formato válido.'))

    _maestro_email_unico = models.Constraint(
        'UNIQUE(email)',
        'Ya existe un maestro registrado con ese correo.',
    )
