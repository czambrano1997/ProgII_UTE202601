from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..services.kodigo_wasi_service import KodigoWasiService
from ..shared.logger import KWLogger

_logger = KWLogger(__name__)


class KWInstructor(models.Model):
    _name = "kw.instructor"
    _description = "Instructor"
    _order = "name"

    # ------------------------------------------------------------------ #
    # Campos                                                               #
    # ------------------------------------------------------------------ #

    name = fields.Char(string="Nombre", required=True)
    especialidad = fields.Char(string="Especialidad")
    email = fields.Char(string="Correo electrónico")
    telefono = fields.Char(string="Teléfono")
    biografia = fields.Text(string="Biografía")
    es_yachak = fields.Boolean(string="Es Yachak (Senior)", default=False)
    activo = fields.Boolean(string="Activo", default=True)

    # Relaciones
    taller_ids = fields.One2many("kw.taller", "instructor_id", string="Talleres")

    # Campos calculados
    total_talleres = fields.Integer(
        string="Total de talleres",
        compute="_compute_estadisticas",
        store=True,
    )
    talleres_activos = fields.Integer(
        string="Talleres activos",
        compute="_compute_estadisticas",
        store=True,
    )

    # ------------------------------------------------------------------ #
    # Computes                                                             #
    # ------------------------------------------------------------------ #

    @api.depends("taller_ids", "taller_ids.activo")
    def _compute_estadisticas(self):
        for instructor in self:
            instructor.total_talleres = len(instructor.taller_ids)
            instructor.talleres_activos = len(
                instructor.taller_ids.filtered(lambda t: t.activo)
            )

    # ------------------------------------------------------------------ #
    # Constraints                                                          #
    # ------------------------------------------------------------------ #

    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            resultado = (
                KodigoWasiService.check_instructor_email(rec.email)
                .alt(_logger.tap_err("Validación email instructor"))
            )
            _logger.raise_validation_if_err(resultado)

    @api.constrains("taller_ids")
    def _check_disponibilidad(self):
        """Evita que el instructor tenga dos talleres con fechas solapadas."""
        for instructor in self:
            for taller in instructor.taller_ids:
                otros_talleres = instructor.taller_ids.filtered(
                    lambda t: t.id != taller.id
                )
                resultado = (
                    KodigoWasiService.check_instructor_disponible(
                        taller.fecha_inicio,
                        taller.fecha_fin,
                        otros_talleres,
                        taller_id_excluir=taller.id,
                    )
                    .alt(_logger.tap_err("Conflicto de agenda instructor"))
                )
                _logger.raise_validation_if_err(resultado)

    # ------------------------------------------------------------------ #
    # Acciones                                                             #
    # ------------------------------------------------------------------ #

    def action_toggle_yachak(self):
        """Alterna la distinción Yachak (Senior) del instructor."""
        for rec in self:
            rec.es_yachak = not rec.es_yachak
            estado = "otorgada" if rec.es_yachak else "retirada"
            _logger.info(
                "Distinción Yachak %s — instructor: %s", estado, rec.name
            )

    def action_archivar(self):
        """Archiva el instructor (activo = False) si no tiene talleres activos."""
        for rec in self:
            if rec.talleres_activos > 0:
                raise ValidationError(
                    f"No se puede archivar a '{rec.name}': tiene "
                    f"{rec.talleres_activos} taller(es) activo(s)."
                )
            rec.activo = False
            _logger.info("Instructor archivado: %s", rec.name)
