from odoo import models, fields, api

class BibliotecaBusqueda(models.Model):
    _name = 'biblioteca.busqueda'
    _description = 'Modelo para búsqueda de libros'

    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    nombre_completo = fields.Char(string='Usuario Completo', compute='_compute_nombre_completo')
    libro_titulo = fields.Char(string='Título del Libro')

    @api.depends('nombre', 'apellido')
    def _compute_nombre_completo(self):
        for record in self:
            # Aquí hacemos la concatenación que practicaste en SQL
            record.nombre_completo = f"{record.nombre} {record.apellido}"
