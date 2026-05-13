"""
shared/logger.py
================
KWLogger — Logger integrado con el pipeline ROP (Railway Oriented Programming).

Responsabilidades
-----------------
  1. **Consola / servidor**  : usa el módulo estándar `logging` de Python.
     Los mensajes aparecen en el log de Odoo (stdout / journald / archivo).

  2. **Cliente web**         : lanza `UserError` o `ValidationError` para que
     Odoo muestre el mensaje en la interfaz del usuario.

  3. **Interoperabilidad ROP**: métodos diseñados para usarse como callbacks
     en `.alt()`, `.map()` y `.bind()` sin romper el flujo del pipeline.

Uso rápido
----------
    from ..shared.logger import KWLogger

    _logger = KWLogger(__name__)

    # --- Flujo Railway ---
    resultado = (
        KodigoWasiService.validar_inscripcion(taller, participante)
        .alt(_logger.tap_err("Inscripción rechazada"))   # log + sigue como Err
    )
    _logger.raise_if_err(resultado)   # lanza UserError si es Err

    # --- Log directo ---
    _logger.info("Inscripción creada para %s", participante.name)
    _logger.error("Fallo inesperado: %s", detalle)
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from odoo.exceptions import UserError, ValidationError

from .result import Err, Ok, Result


# ---------------------------------------------------------------------------
# Logger principal
# ---------------------------------------------------------------------------

class KWLogger:
    """
    Logger de dominio para módulos Kodigowasi.

    Parameters
    ----------
    name : str
        Nombre del logger. Usa ``__name__`` en cada módulo para obtener
        rutas jerárquicas (``kodigowasi.models.kw_inscripcion``, etc.).
    """

    def __init__(self, name: str) -> None:
        self._log = logging.getLogger(name)

    # ------------------------------------------------------------------
    # Logging directo (consola / servidor)
    # ------------------------------------------------------------------

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log.error(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Registra el mensaje **más** el traceback activo."""
        self._log.exception(msg, *args, **kwargs)

    # ------------------------------------------------------------------
    # Integración con el pipeline ROP
    # ------------------------------------------------------------------

    def tap_err(
        self,
        context: str = "",
    ) -> Callable[[Any], Any]:
        """
        Devuelve una función para usar en ``.alt()``.

        Registra el error en consola y lo devuelve **sin modificarlo**,
        dejando el ``Err`` intacto en el pipeline.

        Ejemplo
        -------
            resultado = (
                servicio.validar(...)
                .alt(_logger.tap_err("Validación de cupo"))
            )

        Parameters
        ----------
        context : str
            Etiqueta descriptiva que aparece en el log.
        """
        prefix = f"[{context}] " if context else ""

        def _tap(error: Any) -> Any:
            self._log.error("%s%s", prefix, error)
            return error   # alt espera el error transformado, no Err(error)

        return _tap

    def tap_ok(
        self,
        context: str = "",
    ) -> Callable[[Any], Any]:
        """
        Devuelve una función para usar en ``.map()``.

        Registra el valor exitoso y lo pasa al siguiente paso.

        Ejemplo
        -------
            resultado = (
                servicio.calcular(...)
                .map(_logger.tap_ok("Precio calculado"))
            )
        """
        prefix = f"[{context}] " if context else ""

        def _tap(value: Any) -> Any:
            self._log.info("%s%r", prefix, value)
            return value

        return _tap

    def log_result(
        self,
        result: Result,
        context: str = "",
    ) -> Result:
        """
        Registra el resultado (``Ok`` o ``Err``) y lo devuelve sin cambios.

        Útil para inspeccionar el estado del pipeline en medio de una cadena.

        Ejemplo
        -------
            resultado = _logger.log_result(
                servicio.validar(...),
                context="Validación inscripción",
            )
        """
        prefix = f"[{context}] " if context else ""
        match result:
            case Ok(value=v):
                self._log.info("%sOK → %r", prefix, v)
            case Err(error=e):
                self._log.error("%sERR → %s", prefix, e)
        return result

    # ------------------------------------------------------------------
    # Surfacing de errores al cliente web
    # ------------------------------------------------------------------

    def raise_if_err(
        self,
        result: Result,
        *,
        client_msg: str | None = None,
        use_validation_error: bool = False,
    ) -> Ok:
        """
        Si ``result`` es ``Err``:
          - registra el error en consola/servidor.
          - lanza ``UserError`` (o ``ValidationError``) para que Odoo lo
            muestre en el cliente web.

        Si ``result`` es ``Ok``, lo devuelve sin modificarlo.

        Parameters
        ----------
        result : Result
            El resultado ROP a inspeccionar.
        client_msg : str | None
            Mensaje alternativo para el cliente. Si es ``None`` se usa el
            propio error del ``Err``.
        use_validation_error : bool
            ``True`` → lanza ``ValidationError`` (útil en ``@api.constrains``).
            ``False`` (defecto) → lanza ``UserError`` (para acciones de botón).

        Ejemplo
        -------
            # En un método de botón
            _logger.raise_if_err(
                KodigoWasiService.validar_inscripcion(taller, participante),
                client_msg="No se pudo confirmar la inscripción.",
            )

            # En @api.constrains
            _logger.raise_if_err(
                KodigoWasiService.check_taller_fechas(inicio, fin),
                use_validation_error=True,
            )
        """
        match result:
            case Err(error=e):
                self._log.error("[KW] %s", e)
                msg = client_msg if client_msg is not None else str(e)
                if use_validation_error:
                    raise ValidationError(msg)
                raise UserError(msg)
            case Ok():
                return result

    def raise_validation_if_err(
        self,
        result: Result,
        *,
        client_msg: str | None = None,
    ) -> Ok:
        """
        Atajo para ``raise_if_err(..., use_validation_error=True)``.
        Pensado para usarse exclusivamente dentro de ``@api.constrains``.
        """
        return self.raise_if_err(
            result,
            client_msg=client_msg,
            use_validation_error=True,
        )


__all__ = ["KWLogger"]
