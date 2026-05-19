from odoo import models, fields

class Cliente(models.Model):
    _name = 'choco.cliente'
    _description = 'Clientes'

    nombre = fields.Char(string='Nombre', required=True)
    telefono = fields.Char(string='Telefono')
    correo = fields.Char(string='Correo')
    fecha_registro = fields.Date(string='Fecha Registro')