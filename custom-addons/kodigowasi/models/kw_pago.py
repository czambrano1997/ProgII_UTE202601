from odoo import models, fields, api
from odoo.exceptions import UserError
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWPago(models.Model):
    _name = "kw.pago"
    _description = "Pago de Inscripción"
    _order = "fecha_pago desc"

    # ------------------------------------------------------------------ #
    # Campos                                                               #
    # ------------------------------------------------------------------ #

    inscripcion_id = fields.Many2one(
        "kw.inscripcion",
        string="Inscripción",
        required=True,
        ondelete="cascade",
    )
    monto = fields.Float(string="Monto ($)", required=True, digits=(10, 2))
    fecha_pago = fields.Datetime(
        string="Fecha de pago", default=fields.Datetime.now
    )
    metodo = fields.Selection(
        [
            ("efectivo", "Efectivo"),
            ("transferencia", "Transferencia"),
            ("tarjeta", "Tarjeta"),
        ],
        string="Método de pago",
        default="efectivo",
        required=True,
    )
    referencia = fields.Char(string="Referencia / Comprobante")
    notas = fields.Text(string="Notas internas")
    estado = fields.Selection(
        [
            ("pendiente", "Pendiente verificación"),
            ("verificado", "Verificado"),
            ("rechazado", "Rechazado"),
        ],
        string="Estado",
        default="pendiente",
        required=True,
    )

    # Campos calculados
    taller_nombre = fields.Char(
        string="Taller",
        related="inscripcion_id.taller_id.name",
        store=False,
    )
    participante_nombre = fields.Char(
        string="Participante",
        related="inscripcion_id.participante_id.name",
        store=False,
    )
    total_inscripcion = fields.Float(
        string="Total pagado (inscripción)",
        compute="_compute_total_inscripcion",
        store=False,
        digits=(10, 2),
    )
    pago_completo = fields.Boolean(
        string="Pago completo",
        compute="_compute_total_inscripcion",
        store=False,
    )

    # ------------------------------------------------------------------ #
    # Computes                                                             #
    # ------------------------------------------------------------------ #

    @api.depends("inscripcion_id", "inscripcion_id.pago_ids.monto",
                 "inscripcion_id.taller_id.precio")
    def _compute_total_inscripcion(self):
        for pago in self:
            inscripcion = pago.inscripcion_id
            precio = getattr(inscripcion.taller_id, "precio", 0.0) or 0.0
            total = KodigoWasiService.calcular_total_pagado(
                inscripcion.pago_ids.filtered(lambda p: p.estado != "rechazado")
            )
            pago.total_inscripcion = total
            resultado = KodigoWasiService.check_pago_completo(total, precio)
            pago.pago_completo = bool(resultado)

    # ------------------------------------------------------------------ #
    # Constraints                                                          #
    # ------------------------------------------------------------------ #

    @api.constrains("monto", "inscripcion_id")
    def _check_pago_valido(self):
        for rec in self:
            # Excluir el pago actual del total previo (edición)
            pagos_previos = rec.inscripcion_id.pago_ids.filtered(
                lambda p: p.id != rec.id and p.estado != "rechazado"
            )
            total_previo = KodigoWasiService.calcular_total_pagado(pagos_previos)
            precio_taller = getattr(rec.inscripcion_id.taller_id, "precio", 0.0) or 0.0

            resultado = (
                KodigoWasiService.check_pago_monto_positivo(rec.monto)
                .bind(lambda _: KodigoWasiService.check_pago_no_excede_precio(
                    rec.monto, total_previo, precio_taller
                ))
                .alt(_logger.tap_err("Validación pago"))
            )
            _logger.raise_validation_if_err(resultado)

    # ------------------------------------------------------------------ #
    # Acciones                                                             #
    # ------------------------------------------------------------------ #

    def action_verificar(self):
        """Marca el pago como verificado y actualiza pago_realizado en la inscripción."""
        for rec in self:
            if rec.estado == "rechazado":
                raise UserError("No se puede verificar un pago rechazado.")
            rec.estado = "verificado"
            # Actualizar flag en inscripción si el pago ya cubre el total
            precio = getattr(rec.inscripcion_id.taller_id, "precio", 0.0) or 0.0
            total = KodigoWasiService.calcular_total_pagado(
                rec.inscripcion_id.pago_ids.filtered(
                    lambda p: p.estado != "rechazado"
                )
            )
            if bool(KodigoWasiService.check_pago_completo(total, precio)):
                rec.inscripcion_id.pago_realizado = True
            _logger.info(
                "Pago verificado — $%.2f | inscripción: %s",
                rec.monto,
                rec.inscripcion_id.id,
            )

    def action_rechazar(self):
        """Rechaza el pago y desmarca pago_realizado si es necesario."""
        for rec in self:
            if rec.estado == "verificado":
                raise UserError(
                    "No se puede rechazar un pago ya verificado. "
                    "Contacte al administrador."
                )
            rec.estado = "rechazado"
            # Revisar si la inscripción sigue cubierta
            precio = getattr(rec.inscripcion_id.taller_id, "precio", 0.0) or 0.0
            total = KodigoWasiService.calcular_total_pagado(
                rec.inscripcion_id.pago_ids.filtered(
                    lambda p: p.estado != "rechazado"
                )
            )
            if not bool(KodigoWasiService.check_pago_completo(total, precio)):
                rec.inscripcion_id.pago_realizado = False
            _logger.info(
                "Pago rechazado — $%.2f | inscripción: %s",
                rec.monto,
                rec.inscripcion_id.id,
            )
