"""
tests/test_service.py
=====================
Tests unitarios para KodigoWasiService.

Los métodos puros (check_taller_fechas, check_cupo_disponible,
check_taller_activo, calcular_precio_por_nivel) se prueban directamente.

validar_inscripcion usa recordsets Odoo → se mockea con SimpleNamespace
y MagicMock para simular .filtered() sin necesitar base de datos.

Cada test verifica tanto el camino Ok (éxito) como el Err (error esperado).
"""

import unittest
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from kodigowasi.services.kodigo_wasi_service import KodigoWasiService
from kodigowasi.shared.result import Err, Ok


# ---------------------------------------------------------------------------
# Helpers para construir mocks de recordsets
# ---------------------------------------------------------------------------

def _make_taller(
    *,
    name: str = "Taller Test",
    max_cupos: int = 10,
    confirmadas: int = 0,
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
) -> MagicMock:
    """Simula un recordset kw.taller con los campos mínimos del servicio."""
    taller = MagicMock()
    taller.name = name
    taller.max_cupos = max_cupos
    taller.fecha_inicio = fecha_inicio
    taller.fecha_fin = fecha_fin
    # inscripcion_ids.filtered(...) devuelve una lista con `confirmadas` items
    taller.inscripcion_ids.filtered.return_value = [MagicMock()] * confirmadas
    return taller


def _make_participante(*, ya_confirmado_en: object = None) -> MagicMock:
    """
    Simula un recordset kw.participante.

    ya_confirmado_en : taller mock donde el participante ya tiene confirmación.
                       None → sin inscripciones previas confirmadas.
    """
    participante = MagicMock()

    def _filtered(fn):
        # Reproduce la lambda del servicio:
        # lambda i: i.taller_id == taller and i.estado == 'confirmado'
        if ya_confirmado_en is None:
            return []
        inscripcion = MagicMock()
        inscripcion.taller_id = ya_confirmado_en
        inscripcion.estado = "confirmado"
        return [i for i in [inscripcion] if fn(i)]

    participante.inscripcion_ids.filtered.side_effect = _filtered
    return participante


# ---------------------------------------------------------------------------
# check_taller_fechas
# ---------------------------------------------------------------------------

class TestCheckTallerFechas(unittest.TestCase):

    def test_ok_cuando_fechas_son_none(self):
        """Sin fechas no hay restricción."""
        resultado = KodigoWasiService.check_taller_fechas(None, None)
        self.assertIsInstance(resultado, Ok)

    def test_ok_cuando_solo_inicio(self):
        resultado = KodigoWasiService.check_taller_fechas(date.today(), None)
        self.assertIsInstance(resultado, Ok)

    def test_ok_cuando_solo_fin(self):
        resultado = KodigoWasiService.check_taller_fechas(None, date.today())
        self.assertIsInstance(resultado, Ok)

    def test_ok_fin_posterior_a_inicio(self):
        inicio = date(2025, 1, 1)
        fin = date(2025, 6, 30)
        resultado = KodigoWasiService.check_taller_fechas(inicio, fin)
        self.assertIsInstance(resultado, Ok)

    def test_ok_un_dia_de_diferencia(self):
        inicio = date(2025, 3, 1)
        fin = inicio + timedelta(days=1)
        resultado = KodigoWasiService.check_taller_fechas(inicio, fin)
        self.assertIsInstance(resultado, Ok)

    def test_err_fin_igual_a_inicio(self):
        hoy = date.today()
        resultado = KodigoWasiService.check_taller_fechas(hoy, hoy)
        self.assertIsInstance(resultado, Err)
        self.assertIn("posterior", resultado.error)

    def test_err_fin_antes_de_inicio(self):
        inicio = date(2025, 6, 1)
        fin = date(2025, 1, 1)
        resultado = KodigoWasiService.check_taller_fechas(inicio, fin)
        self.assertIsInstance(resultado, Err)

    def test_err_mensaje_descriptivo(self):
        inicio = date(2025, 5, 10)
        fin = date(2025, 5, 9)
        resultado = KodigoWasiService.check_taller_fechas(inicio, fin)
        self.assertIn("fecha de fin", resultado.error.lower())


# ---------------------------------------------------------------------------
# check_cupo_disponible
# ---------------------------------------------------------------------------

class TestCheckCupoDisponible(unittest.TestCase):

    def test_ok_hay_plazas_libres(self):
        resultado = KodigoWasiService.check_cupo_disponible(10, 5, "Python Básico")
        self.assertIsInstance(resultado, Ok)

    def test_ok_primera_inscripcion(self):
        resultado = KodigoWasiService.check_cupo_disponible(10, 0, "Python Básico")
        self.assertIsInstance(resultado, Ok)

    def test_ok_ultima_plaza(self):
        resultado = KodigoWasiService.check_cupo_disponible(10, 9, "Python Básico")
        self.assertIsInstance(resultado, Ok)

    def test_err_sin_cupo(self):
        resultado = KodigoWasiService.check_cupo_disponible(10, 10, "Python Básico")
        self.assertIsInstance(resultado, Err)
        self.assertIn("Python Básico", resultado.error)

    def test_err_sobre_cupo(self):
        """Plazas ocupadas mayor que max (datos inconsistentes)."""
        resultado = KodigoWasiService.check_cupo_disponible(10, 15, "Python Básico")
        self.assertIsInstance(resultado, Err)

    def test_err_cupo_maximo_cero(self):
        resultado = KodigoWasiService.check_cupo_disponible(0, 0, "Taller Cerrado")
        self.assertIsInstance(resultado, Err)
        self.assertIn("cupo positivo", resultado.error)

    def test_err_cupo_maximo_negativo(self):
        resultado = KodigoWasiService.check_cupo_disponible(-5, 0, "Taller Roto")
        self.assertIsInstance(resultado, Err)

    def test_err_mensaje_incluye_nombre_taller(self):
        resultado = KodigoWasiService.check_cupo_disponible(2, 2, "Rust Avanzado")
        self.assertIn("Rust Avanzado", resultado.error)


# ---------------------------------------------------------------------------
# check_taller_activo
# ---------------------------------------------------------------------------

class TestCheckTallerActivo(unittest.TestCase):

    def test_ok_sin_fecha_inicio(self):
        resultado = KodigoWasiService.check_taller_activo(None, "Taller")
        self.assertIsInstance(resultado, Ok)

    def test_ok_taller_aun_no_comienza_hoy(self):
        """La fecha de inicio es hoy; no ha 'comenzado' aún (today() > inicio es False)."""
        resultado = KodigoWasiService.check_taller_activo(date.today(), "Taller")
        self.assertIsInstance(resultado, Ok)

    def test_ok_taller_comienza_manana(self):
        manana = date.today() + timedelta(days=1)
        resultado = KodigoWasiService.check_taller_activo(manana, "Taller Futuro")
        self.assertIsInstance(resultado, Ok)

    def test_err_taller_ya_comenzo(self):
        ayer = date.today() - timedelta(days=1)
        resultado = KodigoWasiService.check_taller_activo(ayer, "Taller Pasado")
        self.assertIsInstance(resultado, Err)

    def test_err_taller_comenzo_hace_meses(self):
        hace_meses = date.today() - timedelta(days=90)
        resultado = KodigoWasiService.check_taller_activo(hace_meses, "Taller Viejo")
        self.assertIsInstance(resultado, Err)

    def test_err_mensaje_incluye_nombre_taller(self):
        ayer = date.today() - timedelta(days=1)
        resultado = KodigoWasiService.check_taller_activo(ayer, "Django REST")
        self.assertIn("Django REST", resultado.error)
        self.assertIn("ya comenzó", resultado.error)


# ---------------------------------------------------------------------------
# calcular_precio_por_nivel
# ---------------------------------------------------------------------------

class TestCalcularPrecioPorNivel(unittest.TestCase):

    def test_nivel_wawa(self):
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel("wawa"), 50.0)

    def test_nivel_mashi(self):
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel("mashi"), 100.0)

    def test_nivel_yachak(self):
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel("yachak"), 200.0)

    def test_nivel_desconocido_devuelve_cero(self):
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel("ninja"), 0.0)

    def test_nivel_vacio_devuelve_cero(self):
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel(""), 0.0)

    def test_nivel_mayusculas_devuelve_cero(self):
        """Los niveles son case-sensitive."""
        self.assertEqual(KodigoWasiService.calcular_precio_por_nivel("WAWA"), 0.0)


# ---------------------------------------------------------------------------
# validar_inscripcion (con mocks de recordsets)
# ---------------------------------------------------------------------------

class TestValidarInscripcion(unittest.TestCase):

    # --- Caminos Ok ---

    def test_ok_taller_valido_sin_inscripciones_previas(self):
        manana = date.today() + timedelta(days=1)
        taller = _make_taller(
            max_cupos=10,
            confirmadas=0,
            fecha_inicio=manana,
            fecha_fin=manana + timedelta(days=30),
        )
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Ok)

    def test_ok_taller_sin_fechas(self):
        """Taller sin fechas es válido (fechas opcionales)."""
        taller = _make_taller(max_cupos=5, confirmadas=2)
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Ok)

    def test_ok_ultima_plaza_disponible(self):
        manana = date.today() + timedelta(days=1)
        taller = _make_taller(max_cupos=5, confirmadas=4, fecha_inicio=manana)
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Ok)

    # --- Caminos Err ---

    def test_err_taller_sin_cupo(self):
        manana = date.today() + timedelta(days=1)
        taller = _make_taller(max_cupos=5, confirmadas=5, fecha_inicio=manana)
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)
        self.assertIn("cupo", resultado.error.lower())

    def test_err_taller_ya_comenzo(self):
        ayer = date.today() - timedelta(days=1)
        taller = _make_taller(
            max_cupos=10,
            confirmadas=2,
            fecha_inicio=ayer,
            fecha_fin=ayer + timedelta(days=30),
        )
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)
        self.assertIn("ya comenzó", resultado.error)

    def test_err_fechas_invalidas_fin_antes_de_inicio(self):
        taller = _make_taller(
            max_cupos=10,
            confirmadas=0,
            fecha_inicio=date(2025, 12, 31),
            fecha_fin=date(2025, 1, 1),
        )
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)

    def test_err_participante_ya_confirmado(self):
        """Si el participante ya está confirmado en el taller, retorna Err."""
        manana = date.today() + timedelta(days=1)
        taller = _make_taller(max_cupos=10, confirmadas=1, fecha_inicio=manana)
        # participante ya confirmado en ESE taller
        participante = _make_participante(ya_confirmado_en=taller)
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)
        self.assertIn("ya está confirmado", resultado.error)

    def test_err_cortocircuita_en_primera_validacion_fallida(self):
        """combine() devuelve el primer Err; las siguientes no se evalúan."""
        # Cupo = 0 fuerza Err en check_cupo (2ª validación)
        # Pero primero: fechas inválidas (1ª validación)
        taller = _make_taller(
            max_cupos=0,
            confirmadas=0,
            fecha_inicio=date(2025, 12, 1),
            fecha_fin=date(2025, 1, 1),   # fin < inicio → 1ª validación falla
        )
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)
        # Debe ser el error de FECHAS, no de cupo
        self.assertIn("fecha", resultado.error.lower())

    def test_err_cupo_maximo_cero_sin_importar_confirmadas(self):
        taller = _make_taller(max_cupos=0, confirmadas=0)
        participante = _make_participante()
        resultado = KodigoWasiService.validar_inscripcion(taller, participante)
        self.assertIsInstance(resultado, Err)
        self.assertIn("cupo positivo", resultado.error)

    # --- Pipeline Railway sobre validar_inscripcion ---

    def test_pipeline_bind_sobre_resultado_ok(self):
        """Ok de validar_inscripcion permite continuar el pipeline."""
        manana = date.today() + timedelta(days=1)
        taller = _make_taller(max_cupos=10, confirmadas=0, fecha_inicio=manana)
        participante = _make_participante()

        pasos_ejecutados = []

        resultado = (
            KodigoWasiService.validar_inscripcion(taller, participante)
            .map(lambda _: pasos_ejecutados.append("inscripcion_creada") or "inscripcion_creada")
            .map(lambda estado: pasos_ejecutados.append("notificacion_enviada") or estado)
        )

        self.assertIsInstance(resultado, Ok)
        self.assertEqual(pasos_ejecutados, ["inscripcion_creada", "notificacion_enviada"])

    def test_pipeline_alt_sobre_resultado_err(self):
        """Err de validar_inscripcion puede ser transformado con alt."""
        taller = _make_taller(max_cupos=0)
        participante = _make_participante()

        errores_capturados = []

        resultado = (
            KodigoWasiService.validar_inscripcion(taller, participante)
            .alt(lambda e: errores_capturados.append(e) or e.upper())
        )

        self.assertIsInstance(resultado, Err)
        self.assertEqual(len(errores_capturados), 1)
        self.assertEqual(resultado.error, errores_capturados[0].upper())

    def test_pipeline_lash_convierte_err_a_lista_espera(self):
        """Un taller lleno puede redirigir a lista de espera usando lash."""
        taller = _make_taller(max_cupos=5, confirmadas=5)
        participante = _make_participante()

        resultado = (
            KodigoWasiService.validar_inscripcion(taller, participante)
            .lash(lambda _: Ok("lista_espera"))
        )

        self.assertEqual(resultado, Ok("lista_espera"))
