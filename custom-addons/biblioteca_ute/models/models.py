# -*- coding: utf-8 -*-

from odoo import models, fields

class BibliotecaLibro(models.Model):
    _name = 'biblioteca.libro'
    _description = 'Libros de la UTE'

    name = fields.Char(string='Título del Libro', required=True)