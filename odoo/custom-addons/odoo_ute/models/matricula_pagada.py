from odoo import models, fields

class MatriculaPagada(models.Model):
    _name = 'ute.matricula.pagada'
    _description = 'Estudiantes que han pagado matrícula'

    estudiante_id = fields.Many2one(
        string='Estudiante',
        comodel_name='ute.estudiante',
    )
    carrera_id = fields.Many2one(
        string='Carrera',
        comodel_name='ute.carrera',
    )
    fecha_pago = fields.Date(
        string='Fecha de Pago',
    )
    monto_pagado = fields.Float(
        string='Monto Pagado',
    )