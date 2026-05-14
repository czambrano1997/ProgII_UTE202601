from odoo import models, fields, api

class Alumno(models.Model):
    _name = 'odoo_ute.alumno'
    _description = 'Alumno'
    _rec_name = 'name'

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True
    )
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Email')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')

    matricula_ids = fields.One2many(
        'odoo_ute.matricula', 'alumno_id', string='Matrículas'
    )

    @api.depends('nombre', 'apellido')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.apellido}, {record.nombre}" if record.apellido and record.nombre else record.nombre or record.apellido or 'Sin nombre'