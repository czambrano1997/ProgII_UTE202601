from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWSesion(models.Model):
    _name = "kw.sesion"
    _description = "Sesión de Taller"
    _order = "fecha_hora asc, name asc"

    # ------------------------------------------------------------------ #
    # Campos                                                               #
    # ------------------------------------------------------------------ #

    name = fields.Char(string="Título", required=True)
    taller_id = fields.Many2one(
        "kw.taller", string="Taller", required=True, ondelete="cascade"
    )
    instructor_id = fields.Many2one(
        "kw.instructor",
        string="Instructor de sesión",
        ondelete="set null",
        help="Instructor específico para esta sesión. Si está vacío, se usa el del taller.",
    )
    fecha_hora = fields.Datetime(string="Fecha y hora")
    duracion_minutos = fields.Integer(
        string="Duración (min)",
        default=90,
        help="Duración en minutos. Mínimo 30, máximo 480.",
    )
    contenido = fields.Html(string="Contenido / Agenda")
    link_meet = fields.Char(string="Enlace de reunión")
    grabacion_url = fields.Char(string="URL de grabación")
    notas = fields.Text(string="Notas del instructor")
    completada = fields.Boolean(string="Completada", default=False)
    numero_sesion = fields.Integer(
        string="Número de sesión",
        compute="_compute_numero_sesion",
        store=True,
    )

    # ------------------------------------------------------------------ #
    # Computes                                                             #
    # ------------------------------------------------------------------ #

    @api.depends("taller_id", "taller_id.sesion_ids")
    def _compute_numero_sesion(self):
        for sesion in self:
            sesiones_del_taller = sesion.taller_id.sesion_ids.sorted(
                key=lambda s: (s.fecha_hora or datetime.min, s.id)
            )
            idx = list(sesiones_del_taller.ids).index(sesion.id) + 1 if sesion.id in sesiones_del_taller.ids else 0
            sesion.numero_sesion = idx

    @api.onchange("taller_id")
    def _onchange_taller(self):
        """Pre-llena la fecha con la fecha de inicio del taller al seleccionarlo."""
        if self.taller_id and self.taller_id.fecha_inicio:
            self.fecha_hora = datetime.combine(
                self.taller_id.fecha_inicio, datetime.min.time()
            )
        if self.taller_id and not self.instructor_id:
            self.instructor_id = self.taller_id.instructor_id

    # ------------------------------------------------------------------ #
    # Constraints                                                          #
    # ------------------------------------------------------------------ #

    @api.constrains("fecha_hora", "duracion_minutos", "taller_id")
    def _check_sesion_valida(self):
        for rec in self:
            resultado = (
                KodigoWasiService.validar_sesion(rec, rec.taller_id)
                .alt(_logger.tap_err("Validación sesión"))
            )
            _logger.raise_validation_if_err(resultado)

    # ------------------------------------------------------------------ #
    # Acciones                                                             #
    # ------------------------------------------------------------------ #

    def action_marcar_completada(self):
        """Marca la sesión como completada."""
        for rec in self:
            if rec.completada:
                raise UserError(f"La sesión '{rec.name}' ya estaba marcada como completada.")
            rec.completada = True
            _logger.info(
                "Sesión completada — '%s' (taller: %s)",
                rec.name,
                rec.taller_id.name,
            )

    def action_reabrir(self):
        """Reabre una sesión completada (p.ej. para re-grabación o corrección)."""
        for rec in self:
            if not rec.completada:
                raise UserError(f"La sesión '{rec.name}' no estaba marcada como completada.")
            rec.completada = False
            _logger.info(
                "Sesión reabierta — '%s' (taller: %s)",
                rec.name,
                rec.taller_id.name,
            )
