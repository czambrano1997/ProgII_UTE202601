"""
tests/test_result.py
====================
Tests unitarios puros para shared/result.py.

Cubre todas las variantes del tipo Result[T, E]:
  Ok  → map, bind, alt, lash, unwrap, unwrap_or, __bool__
  Err → map, bind, alt, lash, unwrap, unwrap_or, __bool__
  Funciones de módulo: combine, map2, from_exception
  Versiones async de los métodos anteriores

No requiere base de datos ni contexto Odoo.
"""

import unittest
from datetime import date

# Importación directa de los tipos (sin Odoo runtime)
from kodigowasi.shared.result import (
    Err,
    Ok,
    UnwrapError,
    combine,
    from_exception,
    map2,
)


# ---------------------------------------------------------------------------
# Ok
# ---------------------------------------------------------------------------

class TestOk(unittest.TestCase):

    def test_ok_es_truthy(self):
        self.assertTrue(Ok(42))

    def test_ok_unwrap_devuelve_valor(self):
        self.assertEqual(Ok("hola").unwrap(), "hola")

    def test_ok_unwrap_or_devuelve_valor_no_default(self):
        self.assertEqual(Ok(99).unwrap_or(0), 99)

    def test_ok_map_transforma_valor(self):
        resultado = Ok(10).map(lambda x: x * 2)
        self.assertEqual(resultado, Ok(20))

    def test_ok_map_encadena_multiple(self):
        resultado = Ok(3).map(lambda x: x + 1).map(lambda x: x ** 2)
        self.assertEqual(resultado, Ok(16))

    def test_ok_map_err_es_noop(self):
        """Ok no tiene error; map_err no debe tocar el valor."""
        resultado = Ok("valor").map_err(lambda e: "nunca ejecutado")
        self.assertEqual(resultado, Ok("valor"))

    def test_ok_alt_es_noop(self):
        resultado = Ok("valor").alt(lambda e: "nunca")
        self.assertEqual(resultado, Ok("valor"))

    def test_ok_bind_devuelve_ok(self):
        resultado = Ok(5).bind(lambda x: Ok(x + 1))
        self.assertEqual(resultado, Ok(6))

    def test_ok_bind_puede_devolver_err(self):
        resultado = Ok(-1).bind(
            lambda x: Err("negativo") if x < 0 else Ok(x)
        )
        self.assertEqual(resultado, Err("negativo"))

    def test_ok_lash_es_noop(self):
        """Ok ignora la función de recuperación."""
        resultado = Ok("bien").lash(lambda e: Ok("recuperado"))
        self.assertEqual(resultado, Ok("bien"))

    def test_ok_pipeline_completo(self):
        """Simula un pipeline típico Railway sin errores."""
        resultado = (
            Ok(10)
            .map(lambda x: x * 2)
            .bind(lambda x: Ok(x + 5) if x > 0 else Err("negativo"))
            .alt(lambda e: f"error: {e}")
        )
        self.assertEqual(resultado, Ok(25))


# ---------------------------------------------------------------------------
# Err
# ---------------------------------------------------------------------------

class TestErr(unittest.TestCase):

    def test_err_es_falsy(self):
        self.assertFalse(Err("algo salió mal"))

    def test_err_unwrap_lanza_unwrap_error(self):
        with self.assertRaises(UnwrapError) as ctx:
            Err("fallo").unwrap()
        self.assertEqual(ctx.exception.error, "fallo")

    def test_err_unwrap_or_devuelve_default(self):
        self.assertEqual(Err("fallo").unwrap_or("default"), "default")

    def test_err_map_es_noop(self):
        """Err no tiene valor; map no debe ejecutarse."""
        resultado = Err("fallo").map(lambda x: x * 100)
        self.assertEqual(resultado, Err("fallo"))

    def test_err_map_err_transforma_error(self):
        resultado = Err("código 42").map_err(lambda e: e.upper())
        self.assertEqual(resultado, Err("CÓDIGO 42"))

    def test_err_alt_transforma_error(self):
        resultado = Err("minúscula").alt(str.upper)
        self.assertEqual(resultado, Err("MINÚSCULA"))

    def test_err_bind_es_noop(self):
        resultado = Err("fallo").bind(lambda x: Ok(x + 1))
        self.assertEqual(resultado, Err("fallo"))

    def test_err_lash_recupera_a_ok(self):
        resultado = Err("reintentable").lash(lambda e: Ok(f"recuperado desde: {e}"))
        self.assertEqual(resultado, Ok("recuperado desde: reintentable"))

    def test_err_lash_puede_devolver_nuevo_err(self):
        resultado = Err("original").lash(lambda e: Err(f"transformado: {e}"))
        self.assertEqual(resultado, Err("transformado: original"))

    def test_err_pipeline_cortocircuita(self):
        """Una vez en Err, map y bind son no-ops."""
        llamadas = []
        resultado = (
            Err("inicio roto")
            .map(lambda x: llamadas.append("map") or x)
            .bind(lambda x: llamadas.append("bind") or Ok(x))
        )
        self.assertEqual(resultado, Err("inicio roto"))
        self.assertEqual(llamadas, [], "map/bind no deben ejecutarse sobre Err")

    def test_err_lash_luego_map(self):
        """Recuperar un Err permite continuar el pipeline."""
        resultado = (
            Err("cupo lleno")
            .lash(lambda _: Ok(0))   # vuelve a Ok con lista de espera=0
            .map(lambda x: x + 1)    # lista_espera = 1
        )
        self.assertEqual(resultado, Ok(1))


# ---------------------------------------------------------------------------
# UnwrapError
# ---------------------------------------------------------------------------

class TestUnwrapError(unittest.TestCase):

    def test_guarda_error_original(self):
        err = UnwrapError(error={"code": 404})
        self.assertEqual(err.error, {"code": 404})

    def test_mensaje_por_defecto_incluye_repr(self):
        err = UnwrapError(error="sin cupo")
        self.assertIn("sin cupo", str(err))

    def test_mensaje_personalizado(self):
        err = UnwrapError(message="mensaje custom")
        self.assertEqual(str(err), "mensaje custom")

    def test_nothing_sin_error(self):
        err = UnwrapError()
        self.assertIsNone(err.error)
        self.assertIn("Nothing", str(err))


# ---------------------------------------------------------------------------
# Funciones de módulo
# ---------------------------------------------------------------------------

class TestCombine(unittest.TestCase):

    def test_lista_vacia_devuelve_ok_lista_vacia(self):
        self.assertEqual(combine([]), Ok([]))

    def test_todos_ok_devuelve_ok_con_valores(self):
        resultado = combine([Ok(1), Ok(2), Ok(3)])
        self.assertEqual(resultado, Ok([1, 2, 3]))

    def test_primer_err_cortocircuita(self):
        resultado = combine([Ok(1), Err("fallo"), Ok(3)])
        self.assertEqual(resultado, Err("fallo"))

    def test_varios_err_devuelve_el_primero(self):
        resultado = combine([Err("A"), Err("B"), Err("C")])
        self.assertEqual(resultado, Err("A"))

    def test_ok_none_es_valido(self):
        resultado = combine([Ok(None), Ok(None)])
        self.assertEqual(resultado, Ok([None, None]))


class TestMap2(unittest.TestCase):

    def test_dos_ok_combina_con_funcion(self):
        resultado = map2(Ok(3), Ok(4), lambda a, b: a + b)
        self.assertEqual(resultado, Ok(7))

    def test_primer_err_cortocircuita(self):
        resultado = map2(Err("r1 falló"), Ok(4), lambda a, b: a + b)
        self.assertEqual(resultado, Err("r1 falló"))

    def test_segundo_err_cortocircuita(self):
        resultado = map2(Ok(3), Err("r2 falló"), lambda a, b: a + b)
        self.assertEqual(resultado, Err("r2 falló"))

    def test_ambos_err_devuelve_el_primero(self):
        resultado = map2(Err("primero"), Err("segundo"), lambda a, b: a + b)
        self.assertEqual(resultado, Err("primero"))


class TestFromException(unittest.TestCase):

    def test_funcion_exitosa_devuelve_ok(self):
        resultado = from_exception(lambda: int("42"), ValueError)
        self.assertEqual(resultado, Ok(42))

    def test_excepcion_esperada_devuelve_err(self):
        resultado = from_exception(lambda: int("no-es-numero"), ValueError)
        self.assertIsInstance(resultado, Err)
        self.assertIsInstance(resultado.error, ValueError)

    def test_excepcion_no_esperada_se_propaga(self):
        with self.assertRaises(TypeError):
            from_exception(lambda: 1 + "dos", ValueError)  # TypeError, no ValueError

    def test_devuelve_valor_complejo(self):
        resultado = from_exception(lambda: {"clave": "valor"}, KeyError)
        self.assertEqual(resultado, Ok({"clave": "valor"}))


# ---------------------------------------------------------------------------
# Async (via asyncio.run)
# ---------------------------------------------------------------------------

class TestAsync(unittest.IsolatedAsyncioTestCase):

    async def test_ok_map_async(self):
        async def doble(x): return x * 2
        resultado = await Ok(5).map_async(doble)
        self.assertEqual(resultado, Ok(10))

    async def test_ok_bind_async(self):
        async def validar(x):
            return Ok(x) if x > 0 else Err("negativo")
        resultado = await Ok(3).bind_async(validar)
        self.assertEqual(resultado, Ok(3))

    async def test_ok_bind_async_puede_retornar_err(self):
        async def validar(x):
            return Err("negativo") if x < 0 else Ok(x)
        resultado = await Ok(-1).bind_async(validar)
        self.assertEqual(resultado, Err("negativo"))

    async def test_err_map_async_es_noop(self):
        async def doble(x): return x * 2
        resultado = await Err("roto").map_async(doble)
        self.assertEqual(resultado, Err("roto"))

    async def test_err_lash_async_recupera(self):
        async def recuperar(e): return Ok(f"salvado: {e}")
        resultado = await Err("crítico").lash_async(recuperar)
        self.assertEqual(resultado, Ok("salvado: crítico"))

    async def test_err_alt_async_transforma_error(self):
        async def transformar(e): return e.upper()
        resultado = await Err("fallo silencioso").alt_async(transformar)
        self.assertEqual(resultado, Err("FALLO SILENCIOSO"))

    async def test_ok_alt_async_es_noop(self):
        async def transformar(e): return "nunca"
        resultado = await Ok("bien").alt_async(transformar)
        self.assertEqual(resultado, Ok("bien"))

    async def test_ok_lash_async_es_noop(self):
        async def recuperar(e): return Ok("recuperado")
        resultado = await Ok("ya bien").lash_async(recuperar)
        self.assertEqual(resultado, Ok("ya bien"))
