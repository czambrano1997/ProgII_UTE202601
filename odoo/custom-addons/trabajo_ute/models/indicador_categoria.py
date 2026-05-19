<<<<<<< HEAD
# -*- coding: utf-8 -*-
=======
# -- coding: utf-8 --
>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IndicadorCategoria(models.Model):
    _name = 'ou.indicador.categoria'
    _description = 'Categoría de Indicador de Calificación'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre de Categoría', required=True, tracking=True)
    code = fields.Char(string='Código', required=True, copy=False)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo', default=True)
    tipo_indicador = fields.Selection([
        ('conductor', 'Conductor'),
        ('vehiculo', 'Vehículo'),
        ('general', 'General'),
    ], string='Tipo de Indicador', required=True, default='general', tracking=True)
    peso_porcentaje = fields.Float(string='Peso (%)', required=True, default=0.0)
    color = fields.Integer(string='Color', default=0)
    
    # Campos relacionales
    subcategoria_ids = fields.One2many(
        'ou.indicador.subcategoria', 
        'categoria_id', 
        string='Subcategorías'
    )
    total_subcategorias = fields.Integer(
        string='Total Subcategorías', 
        compute='_compute_total_subcategorias', 
        store=True
    )

    @api.depends('subcategoria_ids')
    def _compute_total_subcategorias(self):
        for record in self:
            record.total_subcategorias = len(record.subcategoria_ids)

    @api.constrains('peso_porcentaje')
    def _check_peso_porcentaje(self):
        for record in self:
            if record.peso_porcentaje < 0 or record.peso_porcentaje > 100:
                raise ValidationError('El peso porcentual debe estar entre 0 y 100.')

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.search_count([('code', '=', record.code), ('id', '!=', record.id)]) > 0:
                raise ValidationError('El código de categoría debe ser único.')

    @api.onchange('tipo_indicador')
    def _onchange_tipo_indicador(self):
        if self.tipo_indicador == 'conductor':
            return {'warning': {
                'title': 'Atención',
                'message': 'Los indicadores de conductor requieren evaluación mensual obligatoria.'
            }}

<<<<<<< HEAD
=======
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'El código de la categoría debe ser único.'),
    ]

>>>>>>> c1b48e8873a20a5a1324a750d1a52238c1f0fcc6

class IndicadorSubcategoria(models.Model):
    _name = 'ou.indicador.subcategoria'
    _description = 'Subcategoría de Indicador'

    name = fields.Char(string='Nombre', required=True)
    categoria_id = fields.Many2one(
        'ou.indicador.categoria', 
        string='Categoría Padre', 
        required=True, 
        ondelete='cascade'
    )
    descripcion = fields.Text(string='Descripción')
    puntaje_maximo = fields.Float(string='Puntaje Máximo', required=True, default=10.0)