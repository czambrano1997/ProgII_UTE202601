"""
tests/test_logger.py
====================
Tests unitarios para shared/logger.py.

Verifica que KWLogger:
  - Delega correctamente al logger estándar de Python (sin efecto en consola)
  - tap_err: loguea el error y NO modifica el Err en el pipeline
  - tap_ok: loguea el valor y NO modifica el Ok en el pipeline
  - log_result: loguea y devuelve el resultado sin cambios
  - raise_if_err: lanza UserError (o ValidationError) si es Err, devuelve Ok si no
  - raise_validation_if_err: atajo para ValidationError

No requiere base de datos Odoo.
"""

import unittest
from unittest.mock import MagicMock, patch, call

from odoo.exceptions import UserError, ValidationError

from kodigowasi.shared.logger import KWLogger
from kodigowasi.shared.result import Err, Ok


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

def _logger_with_mock() -> tuple[KWLogger, MagicMock]:
    """Devuelve un KWLogger cuyo _log interno está mockeado."""
    logger = KWLogger("kodigowasi.tests")
    mock_log = MagicMock()
    logger._log = mock_log
    return logger, mock_log


# ---------------------------------------------------------------------------
# Métodos de logging directo
# ---------------------------------------------------------------------------

class TestLoggingDirecto(unittest.TestCase):

    def test_info_llama_log_info(self):
        logger, mock_log = _logger_with_mock()
        logger.info("Taller creado: %s", "Python")
        mock_log.info.assert_called_once_with("Taller creado: %s", "Python")

    def test_warning_llama_log_warning(self):
        logger, mock_log = _logger_with_mock()
        logger.warning("Cupo bajo: %d restantes", 2)
        mock_log.warning.assert_called_once_with("Cupo bajo: %d restantes", 2)

    def test_error_llama_log_error(self):
        logger, mock_log = _logger_with_mock()
        logger.error("Error crítico: %s", "timeout")
        mock_log.error.assert_called_once_with("Error crítico: %s", "timeout")

    def test_debug_llama_log_debug(self):
        logger, mock_log = _logger_with_mock()
        logger.debug("debug payload: %r", {"k": "v"})
        mock_log.debug.assert_called_once_with("debug payload: %r", {"k": "v"})

    def test_exception_llama_log_exception(self):
        logger, mock_log = _logger_with_mock()
        logger.exception("Excepción no controlada")
        mock_log.exception.assert_called_once_with("Excepción no controlada")

    def test_nombre_logger_viene_de_name(self):
        import logging
        logger = KWLogger("kodigowasi.models.kw_taller")
        self.assertEqual(logger._log.name, "kodigowasi.models.kw_taller")


# ---------------------------------------------------------------------------
# tap_err
# ---------------------------------------------------------------------------

class TestTapErr(unittest.TestCase):

    def test_tap_err_loguea_el_error(self):
        logger, mock_log = _logger_with_mock()
        tap = logger.tap_err("ctx")
        tap("error de prueba")
        mock_log.error.assert_called_once()
        args = mock_log.error.call_args[0]
        self.assertIn("error de prueba", str(args))

    def test_tap_err_devuelve_mismo_error(self):
        logger, _ = _logger_with_mock()
        tap = logger.tap_err()
        devuelto = tap("sin cupo")
        self.assertEqual(devuelto, "sin cupo")

    def test_tap_err_en_pipeline_preserva_err(self):
        logger, mock_log = _logger_with_mock()
        resultado = Err("taller lleno").alt(logger.tap_err("validación"))
        self.assertIsInstance(resultado, Err)
        self.assertEqual(resultado.error, "taller lleno")
        mock_log.error.assert_called_once()

    def test_tap_err_no_ejecuta_sobre_ok(self):
        logger, mock_log = _logger_with_mock()
        resultado = Ok("todo bien").alt(logger.tap_err("ctx"))
        self.assertIsInstance(resultado, Ok)
        mock_log.error.assert_not_called()

    def test_tap_err_incluye_contexto_en_log(self):
        logger, mock_log = _logger_with_mock()
        logger.tap_err("Inscripción rechazada")("error x")
        args = mock_log.error.call_args[0]
        joined = "".join(str(a) for a in args)
        self.assertIn("Inscripción rechazada", joined)

    def test_tap_err_sin_contexto_no_falla(self):
        logger, mock_log = _logger_with_mock()
        tap = logger.tap_err()   # sin contexto
        tap("error sin contexto")
        mock_log.error.assert_called_once()

    def test_tap_err_funciona_con_error_no_string(self):
        logger, _ = _logger_with_mock()
        error_obj = {"code": 404, "msg": "not found"}
        tap = logger.tap_err()
        devuelto = tap(error_obj)
        self.assertEqual(devuelto, error_obj)


# ---------------------------------------------------------------------------
# tap_ok
# ---------------------------------------------------------------------------

class TestTapOk(unittest.TestCase):

    def test_tap_ok_loguea_el_valor(self):
        logger, mock_log = _logger_with_mock()
        tap = logger.tap_ok("ctx")
        tap(42)
        mock_log.info.assert_called_once()

    def test_tap_ok_devuelve_mismo_valor(self):
        logger, _ = _logger_with_mock()
        tap = logger.tap_ok()
        devuelto = tap("precio calculado")
        self.assertEqual(devuelto, "precio calculado")

    def test_tap_ok_en_pipeline_preserva_ok(self):
        logger, mock_log = _logger_with_mock()
        resultado = Ok("inscripcion_ok").map(logger.tap_ok("paso final"))
        self.assertIsInstance(resultado, Ok)
        self.assertEqual(resultado.value, "inscripcion_ok")
        mock_log.info.assert_called_once()

    def test_tap_ok_no_ejecuta_sobre_err(self):
        logger, mock_log = _logger_with_mock()
        resultado = Err("fallo").map(logger.tap_ok("ctx"))
        self.assertIsInstance(resultado, Err)
        mock_log.info.assert_not_called()

    def test_tap_ok_incluye_contexto(self):
        logger, mock_log = _logger_with_mock()
        logger.tap_ok("Precio OK")(99.0)
        args = mock_log.info.call_args[0]
        joined = "".join(str(a) for a in args)
        self.assertIn("Precio OK", joined)


# ---------------------------------------------------------------------------
# log_result
# ---------------------------------------------------------------------------

class TestLogResult(unittest.TestCase):

    def test_ok_loguea_info_y_devuelve_mismo_resultado(self):
        logger, mock_log = _logger_with_mock()
        original = Ok("valor_ok")
        devuelto = logger.log_result(original, "contexto test")
        mock_log.info.assert_called_once()
        self.assertIs(devuelto, original)

    def test_err_loguea_error_y_devuelve_mismo_resultado(self):
        logger, mock_log = _logger_with_mock()
        original = Err("fallo_test")
        devuelto = logger.log_result(original, "contexto test")
        mock_log.error.assert_called_once()
        self.assertIs(devuelto, original)

    def test_ok_sin_contexto_no_falla(self):
        logger, mock_log = _logger_with_mock()
        logger.log_result(Ok(None))
        mock_log.info.assert_called_once()

    def test_err_sin_contexto_no_falla(self):
        logger, mock_log = _logger_with_mock()
        logger.log_result(Err("x"))
        mock_log.error.assert_called_once()

    def test_contexto_aparece_en_log_ok(self):
        logger, mock_log = _logger_with_mock()
        logger.log_result(Ok(1), "mi contexto")
        args = mock_log.info.call_args[0]
        joined = "".join(str(a) for a in args)
        self.assertIn("mi contexto", joined)

    def test_contexto_aparece_en_log_err(self):
        logger, mock_log = _logger_with_mock()
        logger.log_result(Err("e"), "mi contexto")
        args = mock_log.error.call_args[0]
        joined = "".join(str(a) for a in args)
        self.assertIn("mi contexto", joined)


# ---------------------------------------------------------------------------
# raise_if_err
# ---------------------------------------------------------------------------

class TestRaiseIfErr(unittest.TestCase):

    def test_ok_devuelve_ok_sin_lanzar(self):
        logger, _ = _logger_with_mock()
        resultado = logger.raise_if_err(Ok("exito"))
        self.assertIsInstance(resultado, Ok)

    def test_err_lanza_user_error_por_defecto(self):
        logger, mock_log = _logger_with_mock()
        with self.assertRaises(UserError) as ctx:
            logger.raise_if_err(Err("sin cupo"))
        self.assertIn("sin cupo", str(ctx.exception))

    def test_err_loguea_en_consola_antes_de_lanzar(self):
        logger, mock_log = _logger_with_mock()
        with self.assertRaises(UserError):
            logger.raise_if_err(Err("error logueado"))
        mock_log.error.assert_called_once()

    def test_err_usa_client_msg_personalizado(self):
        logger, _ = _logger_with_mock()
        with self.assertRaises(UserError) as ctx:
            logger.raise_if_err(Err("técnico interno"), client_msg="Operación no disponible")
        self.assertIn("Operación no disponible", str(ctx.exception))

    def test_err_validation_error_cuando_se_solicita(self):
        logger, _ = _logger_with_mock()
        with self.assertRaises(ValidationError):
            logger.raise_if_err(Err("fecha inválida"), use_validation_error=True)

    def test_err_client_msg_no_expone_error_tecnico(self):
        """El error interno no debe llegar al cliente si hay client_msg."""
        logger, _ = _logger_with_mock()
        error_tecnico = "DB constraint violation on table kw_taller"
        with self.assertRaises(UserError) as ctx:
            logger.raise_if_err(Err(error_tecnico), client_msg="Error al guardar el taller")
        self.assertNotIn(error_tecnico, str(ctx.exception))
        self.assertIn("Error al guardar el taller", str(ctx.exception))


# ---------------------------------------------------------------------------
# raise_validation_if_err (atajo)
# ---------------------------------------------------------------------------

class TestRaiseValidationIfErr(unittest.TestCase):

    def test_ok_devuelve_ok(self):
        logger, _ = _logger_with_mock()
        resultado = logger.raise_validation_if_err(Ok(None))
        self.assertIsInstance(resultado, Ok)

    def test_err_lanza_validation_error(self):
        logger, _ = _logger_with_mock()
        with self.assertRaises(ValidationError):
            logger.raise_validation_if_err(Err("fecha fin inválida"))

    def test_err_no_lanza_user_error(self):
        """Debe ser ValidationError, no UserError base."""
        logger, _ = _logger_with_mock()
        with self.assertRaises(ValidationError):
            logger.raise_validation_if_err(Err("x"))
        # Si llegamos aquí, no lanzó UserError directo (que no es VE)

    def test_err_client_msg_personalizado(self):
        logger, _ = _logger_with_mock()
        with self.assertRaises(ValidationError) as ctx:
            logger.raise_validation_if_err(
                Err("interno"),
                client_msg="La fecha de fin debe ser posterior al inicio.",
            )
        self.assertIn("La fecha de fin debe ser posterior al inicio.", str(ctx.exception))

    def test_err_loguea_en_consola(self):
        logger, mock_log = _logger_with_mock()
        with self.assertRaises(ValidationError):
            logger.raise_validation_if_err(Err("constraint violada"))
        mock_log.error.assert_called_once()


# ---------------------------------------------------------------------------
# Pipeline integrado: service + logger
# ---------------------------------------------------------------------------

class TestPipelineIntegrado(unittest.TestCase):
    """
    Valida que tap_err + raise_if_err funcionan juntos como en los modelos reales.
    """

    def _validar_fechas(self, inicio, fin):
        from kodigowasi.services.kodigo_wasi_service import KodigoWasiService
        from datetime import date
        return KodigoWasiService.check_taller_fechas(inicio, fin)

    def test_pipeline_ok_no_loguea_error_no_lanza(self):
        from datetime import date
        logger, mock_log = _logger_with_mock()
        from kodigowasi.services.kodigo_wasi_service import KodigoWasiService
        resultado = (
            KodigoWasiService.check_taller_fechas(date(2025, 1, 1), date(2025, 6, 1))
            .alt(logger.tap_err("Fechas taller"))
        )
        logger.raise_validation_if_err(resultado)   # no debe lanzar
        mock_log.error.assert_not_called()

    def test_pipeline_err_loguea_y_lanza(self):
        from datetime import date
        logger, mock_log = _logger_with_mock()
        from kodigowasi.services.kodigo_wasi_service import KodigoWasiService
        resultado = (
            KodigoWasiService.check_taller_fechas(date(2025, 6, 1), date(2025, 1, 1))
            .alt(logger.tap_err("Fechas taller"))
        )
        with self.assertRaises(ValidationError):
            logger.raise_validation_if_err(resultado)
        mock_log.error.assert_called_once()
