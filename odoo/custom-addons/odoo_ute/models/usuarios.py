from odoo import models, fields


class Usuarios(models.Model):
    _name = 'sistema.usuarios'
    _description = 'Usuarios del sistema'

    name = fields.Char(string='Nombre', required=True)
    last_name = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Correo electrónico')
    phone = fields.Char(string='Teléfono')
    vat = fields.Char(string='CI/RUC', size=13)
