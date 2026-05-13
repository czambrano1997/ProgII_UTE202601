from odoo import models, fields, api
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWTaller(models.Model):
    _name = 'kw.taller'
    _description = 'Taller de Programación'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Html(string='Descripción')
    coding_level = fields.Selection([
        ('wawa', 'Wawa (Principiante)'),
        ('mashi', 'Mashi (Intermedio)'),
        ('yachak', 'Yachak (Avanzado)'),
    ], string='Nivel', required=True, default='wawa')
    max_cupos = fields.Integer(string='Cupo máximo', required=True, default=10)
    fecha_inicio = fields.Date(string='Fecha de inicio')
    fecha_fin = fields.Date(string='Fecha de fin')
    precio = fields.Float(string='Precio ($)')
    activo = fields.Boolean(string='Activo', default=True)
    modalidad = fields.Selection([
        ('virtual', 'Virtual'),
        ('presencial', 'Presencial'),
        ('hibrido', 'Híbrido'),
    ], string='Modalidad', default='virtual')
    instructor_id = fields.Many2one('kw.instructor', string='Instructor', ondelete='restrict')
    sesion_ids = fields.One2many('kw.sesion', 'taller_id', string='Sesiones')
    inscripcion_ids = fields.One2many('kw.inscripcion', 'taller_id', string='Inscripciones')
    plazas_disponibles = fields.Integer(
        string='Plazas disponibles',
        compute='_compute_plazas_disponibles',
        store=True,
    )

    @api.depends('max_cupos', 'inscripcion_ids.estado')
    def _compute_plazas_disponibles(self):
        for taller in self:
            confirmadas = taller.inscripcion_ids.filtered(lambda i: i.estado == 'confirmado')
            taller.plazas_disponibles = taller.max_cupos - len(confirmadas)

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for rec in self:
            resultado = (
                KodigoWasiService.check_taller_fechas(rec.fecha_inicio, rec.fecha_fin)
                .alt(_logger.tap_err("Validación fechas taller"))  # log en consola
            )
            # lanza ValidationError (visible en cliente) si es Err
            _logger.raise_validation_if_err(resultado)
