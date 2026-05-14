from odoo import models, fields

class Cursos(models.Model):
    _name = 'odoo_ute.cursos'
    _description = 'Curso'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre del curso', required=True)
    descripcion = fields.Text(string='Descripción')
    creditos = fields.Integer(string='Créditos')
    maestro_id = fields.Many2one(
        'odoo_ute.maestro',
        string='Maestro',
        required=True,
        ondelete='cascade'
    )

    matricula_ids = fields.One2many(
        'odoo_ute.matricula', 'curso_id', string='Matrículas'
    )
    horario_ids = fields.One2many(
        'odoo_ute.horarios', 'curso_id', string='Horarios'
    )