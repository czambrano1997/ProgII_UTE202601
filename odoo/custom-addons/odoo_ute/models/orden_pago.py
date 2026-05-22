from odoo import models, fields

class OrdenPago(models.Model):
    _name = 'ute.orden.pago'
    _description = 'Orden de Pago de Matrícula'

    estudiante_id = fields.Many2one(
        string='Estudiante',
        comodel_name='ute.estudiante',
    )
    carrera_id = fields.Many2one(
        string='Carrera',
        comodel_name='ute.carrera',
    )
    fecha_emision = fields.Date(
        string='Fecha de Emisión',
    )
    monto = fields.Float(
        string='Monto',
    )
    state = fields.Selection(
        string='Estado',
        selection=[
            ('borrador', 'Borrador'),
            ('pagada', 'Pagada'),
        ],
        default='borrador',
    )