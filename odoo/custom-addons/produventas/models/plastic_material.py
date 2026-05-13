# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.from odoo.exceptions import UserError, ValidationError


class Material(models.Model):
    _name = 'plastic.material'
    _description = 'Materia Prima'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    
    name = fields.Char(
        string='Nombre del Material',
        required=True,
        tracking=True,
        help='Nombre comercial del material plástico'
    )
    code = fields.Char(
        string='Código',
        required=True,
        copy=False,
        default=lambda self:('Nuevo')
    )



