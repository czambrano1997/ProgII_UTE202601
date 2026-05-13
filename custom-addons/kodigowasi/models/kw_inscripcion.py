from odoo import models, fields, api
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWInscripcion(models.Model):
    _name = 'kw.inscripcion'
    _description = 'Inscripción a Taller'

    taller_id = fields.Many2one('kw.taller', string='Taller', required=True, ondelete='cascade')
    participante_id = fields.Many2one('kw.participante', string='Participante', required=True, ondelete='restrict')
    fecha_inscripcion = fields.Datetime(string='Fecha de inscripción', default=fields.Datetime.now)
    estado = fields.Selection([
        ('interesado', 'Interesado'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('completado', 'Completado'),
    ], string='Estado', default='interesado', required=True)
    pago_realizado = fields.Boolean(string='Pago realizado')
    codigo_qr = fields.Char(string='Código QR')
    pago_ids = fields.One2many('kw.pago', 'inscripcion_id', string='Pagos')

    @api.constrains('taller_id', 'participante_id', 'estado')
    def _check_inscripcion(self):
        for rec in self:
            if rec.estado == 'confirmado':
                resultado = (
                    KodigoWasiService.validar_inscripcion(rec.taller_id, rec.participante_id)
                    .alt(_logger.tap_err("Validación inscripción"))  # log en consola
                )
                # lanza ValidationError (visible en cliente) si es Err
                _logger.raise_validation_if_err(resultado)

    def action_confirmar(self):
        self.estado = 'confirmado'
        _logger.info(
            "Inscripción confirmada — participante: %s, taller: %s",
            self.participante_id.name,
            self.taller_id.name,
        )

    def action_cancelar(self):
        self.estado = 'cancelado'
        _logger.info(
            "Inscripción cancelada — participante: %s, taller: %s",
            self.participante_id.name,
            self.taller_id.name,
        )
