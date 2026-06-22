# -*- coding: utf-8 -*-
from odoo import models, fields


class TeatroObra(models.Model):
    _name = 'teatro.obra'
    _description = 'Obra de teatro'
    _order = 'name'

    name = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    duracion_minutos = fields.Integer(string='Duración (minutos)')
    genero = fields.Selection(
        [
            ('drama', 'Drama'),
            ('comedia', 'Comedia'),
            ('musical', 'Musical'),
            ('thriller', 'Thriller'),
            ('infantil', 'Infantil'),
            ('otro', 'Otro'),
        ],
        string='Género',
        default='drama',
    )
    estado = fields.Selection(
        [
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
        ],
        string='Estado',
        default='activo',
    )
    funciones_ids = fields.One2many(
        comodel_name='teatro.funcion',
        inverse_name='obra_id',
        string='Funciones',
    )
