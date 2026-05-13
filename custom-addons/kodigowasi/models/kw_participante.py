from odoo import models, fields, api
from odoo.exceptions import UserError
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWParticipante(models.Model):
    _name = "kw.participante"
    _description = "Participante"
    _order = "name"

    # ------------------------------------------------------------------ #
    # Campos                                                               #
    # ------------------------------------------------------------------ #

    name = fields.Char(string="Nombre completo", required=True)
    email = fields.Char(string="Correo electrónico")
    telefono = fields.Char(string="Teléfono")
    cedula = fields.Char(string="Cédula")
    ciudad = fields.Char(string="Ciudad")
    github_usuario = fields.Char(string="Usuario de GitHub")
    nivel_actual = fields.Selection(
        [
            ("wawa", "Wawa (Principiante)"),
            ("mashi", "Mashi (Intermedio)"),
            ("yachak", "Yachak (Avanzado)"),
        ],
        string="Nivel actual",
        default="wawa",
        required=True,
    )
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    activo = fields.Boolean(string="Activo", default=True)

    # Relaciones
    inscripcion_ids = fields.One2many(
        "kw.inscripcion", "participante_id", string="Inscripciones"
    )

    # Campos calculados
    total_inscripciones = fields.Integer(
        string="Total inscripciones",
        compute="_compute_estadisticas",
        store=True,
    )
    inscripciones_confirmadas = fields.Integer(
        string="Confirmadas",
        compute="_compute_estadisticas",
        store=True,
    )
    inscripciones_completadas = fields.Integer(
        string="Completadas",
        compute="_compute_estadisticas",
        store=True,
    )
    puede_ascender = fields.Boolean(
        string="Puede subir de nivel",
        compute="_compute_puede_ascender",
        store=False,
    )

    # ------------------------------------------------------------------ #
    # Computes                                                             #
    # ------------------------------------------------------------------ #

    @api.depends("inscripcion_ids", "inscripcion_ids.estado")
    def _compute_estadisticas(self):
        for p in self:
            p.total_inscripciones = len(p.inscripcion_ids)
            p.inscripciones_confirmadas = len(
                p.inscripcion_ids.filtered(lambda i: i.estado == "confirmado")
            )
            p.inscripciones_completadas = len(
                p.inscripcion_ids.filtered(lambda i: i.estado == "completado")
            )

    @api.depends("nivel_actual", "inscripcion_ids", "inscripcion_ids.estado",
                 "inscripcion_ids.taller_id.coding_level")
    def _compute_puede_ascender(self):
        for p in self:
            resultado = KodigoWasiService.puede_subir_nivel(p)
            p.puede_ascender = bool(resultado)

    # ------------------------------------------------------------------ #
    # Constraints                                                          #
    # ------------------------------------------------------------------ #

    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            resultado = (
                KodigoWasiService.check_participante_email(rec.email)
                .alt(_logger.tap_err("Validación email participante"))
            )
            _logger.raise_validation_if_err(resultado)

    @api.constrains("cedula")
    def _check_cedula(self):
        for rec in self:
            resultado = (
                KodigoWasiService.check_cedula_ecuatoriana(rec.cedula)
                .alt(_logger.tap_err("Validación cédula"))
            )
            _logger.raise_validation_if_err(resultado)

    @api.constrains("fecha_nacimiento")
    def _check_edad(self):
        for rec in self:
            resultado = (
                KodigoWasiService.check_edad_minima(rec.fecha_nacimiento)
                .alt(_logger.tap_err("Validación edad mínima"))
            )
            _logger.raise_validation_if_err(resultado)

    # ------------------------------------------------------------------ #
    # Acciones                                                             #
    # ------------------------------------------------------------------ #

    def action_subir_nivel(self):
        """
        Asciende al participante al siguiente nivel si cumple los requisitos.

        Utiliza el pipeline Railway: si puede_subir_nivel devuelve Ok, actualiza
        el nivel; si devuelve Err, lanza UserError con el motivo.
        """
        for rec in self:
            resultado = (
                KodigoWasiService.puede_subir_nivel(rec)
                .alt(_logger.tap_err("Intento de subir nivel"))
            )
            nivel_nuevo = _logger.raise_if_err(resultado).value
            nivel_anterior = rec.nivel_actual
            rec.nivel_actual = nivel_nuevo
            _logger.info(
                "Nivel actualizado — participante: %s | %s → %s",
                rec.name,
                nivel_anterior,
                nivel_nuevo,
            )

    def action_desactivar(self):
        """Desactiva al participante si no tiene inscripciones confirmadas activas."""
        for rec in self:
            if rec.inscripciones_confirmadas > 0:
                raise UserError(
                    f"'{rec.name}' tiene {rec.inscripciones_confirmadas} inscripción(es) "
                    f"confirmada(s). Cancélalas antes de desactivar al participante."
                )
            rec.activo = False
            _logger.info("Participante desactivado: %s", rec.name)
