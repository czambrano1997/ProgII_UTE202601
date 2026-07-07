from odoo import models, fields, api

class Maestro(models.Model):
    _name = 'odoo_ute.maestro'
    _description = 'Maestro'
    _rec_name = 'name'

    name = fields.Char(
        string='Nombre completo',
        compute='_compute_name',
        store=True
    )
    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    email = fields.Char(string='Email')
    especialidad = fields.Char(string='Especialidad')

    curso_ids = fields.One2many(
        'odoo_ute.cursos', 'maestro_id', string='Cursos impartidos'
    )

    @api.depends('nombre', 'apellido')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.apellido}, {record.nombre}" if record.apellido and record.nombre else record.nombre or record.apellido or 'Sin nombre'