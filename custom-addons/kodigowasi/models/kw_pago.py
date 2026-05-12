from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KWPago(models.Model):
    _name = 'kw.pago'
    _description = 'Pago de Inscripción'

    inscripcion_id = fields.Many2one('kw.inscripcion', string='Inscripción', required=True, ondelete='cascade')
    monto = fields.Float(string='Monto', required=True, digits=(10, 2))
    fecha_pago = fields.Datetime(string='Fecha de pago', default=fields.Datetime.now)
    metodo = fields.Selection([
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta'),
    ], string='Método de pago', default='efectivo')
    referencia = fields.Char(string='Referencia')

    @api.constrains('monto')
    def _check_monto(self):
        for rec in self:
            if rec.monto <= 0:
                raise ValidationError("El monto debe ser mayor que cero.")