"""
shared/result.py
================
Result[T, E] — tipo funcional para manejo explícito de errores.

Variantes
---------
  Ok[T]   — operación exitosa; contiene un valor de tipo T.
  Err[E]  — operación fallida; contiene un error de tipo E.

Alias público
-------------
  Result[T, E] = Ok[T] | Err[E]

Novedades en esta versión:
* UnwrapError guarda el error original para inspección programática.
* Métodos añadidos: alt (transforma el error), lash (recupera desde Err).
* Versiones asíncronas de map, bind, alt y lash.

Funciones de módulo
-------------------
  map2(r1, r2, f)        — combina dos Ok con f(a, b); devuelve el primer Err.
  combine(results)       — list[Result] → Result[list[T]]; cortocircuita en Err.
  from_exception(f, t)   — ejecuta f(); captura exc de tipo t y devuelve Err(e).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------------------
# Excepción de dominio
# ---------------------------------------------------------------------------

class UnwrapError(Exception):
    """
    Lanzada al llamar .unwrap() sobre un Err o Nothing.

    Attributes
    ----------
    error : Any | None
        El error original encapsulado (solo en Err.unwrap).
    """

    def __init__(self, error: Any = None, message: str = "") -> None:
        self.error = error
        if message:
            msg = message
        elif error is not None:
            msg = f"unwrap() llamado sobre Err — error: {error!r}"
        else:
            msg = "unwrap() llamado sobre Nothing"
        super().__init__(msg)


# ---------------------------------------------------------------------------
# Variante exitosa
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Ok[T]:
    value: T

    # Transformaciones sobre el valor ↘
    def map[U](self, f: Callable[[T], U]) -> Ok[U]:
        return Ok(f(self.value))

    def map_err[F](self, f: Callable[[Any], F]) -> Ok[T]:
        """No‑op: Ok no contiene error."""
        return self

    def alt[F](self, f: Callable[[Any], F]) -> Ok[T]:
        """Alias de map_err (terminología Railway)."""
        return self

    def bind[U, E](self, f: Callable[[T], Ok[U] | Err[E]]) -> Ok[U] | Err[E]:
        return f(self.value)

    def lash[F](self, f: Callable[[Any], Ok[T] | Err[F]]) -> Ok[T]:
        """No‑op: Ok ignora la función de recuperación de error."""
        return self

    # Extracción
    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:  # noqa: ARG002
        return self.value

    # Asíncronas
    async def map_async[U](self, f: Callable[[T], Awaitable[U]]) -> Ok[U]:
        return Ok(await f(self.value))

    async def bind_async[U, E](
        self, f: Callable[[T], Awaitable[Ok[U] | Err[E]]]
    ) -> Ok[U] | Err[E]:
        return await f(self.value)

    async def alt_async[F](
        self, f: Callable[[Any], Awaitable[F]]
    ) -> Ok[T]:
        """No‑op asíncrono del alt."""
        return self

    async def lash_async[F](
        self, f: Callable[[Any], Awaitable[Ok[T] | Err[F]]]
    ) -> Ok[T]:
        """No‑op asíncrono del lash."""
        return self

    def __bool__(self) -> bool:
        return True


# ---------------------------------------------------------------------------
# Variante fallida
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Err[E]:
    error: E

    # Transformaciones — todas son no‑op sobre el valor ausente
    def map[T, U](self, f: Callable[[T], U]) -> Err[E]:  # noqa: ARG002
        return self

    def map_err[F](self, f: Callable[[E], F]) -> Err[F]:
        return Err(f(self.error))

    def alt[F](self, f: Callable[[E], F]) -> Err[F]:
        """Transforma el error con *f* (alias de map_err)."""
        return self.map_err(f)

    def bind[T, U](
        self, f: Callable[[T], Ok[U] | Err[E]]  # noqa: ARG002
    ) -> Err[E]:
        return self

    def lash[F](self, f: Callable[[E], Ok[F] | Err[F]]) -> Ok[F] | Err[F]:
        """
        Recuperación desde error: aplica *f* al error.
        Permite volver a la vía exitosa retornando Ok.
        """
        return f(self.error)

    # Extracción
    def unwrap[T](self) -> T:
        raise UnwrapError(self.error)

    def unwrap_or[T](self, default: T) -> T:
        return default

    # Asíncronas
    async def map_async[T, U](
        self, f: Callable[[T], Awaitable[U]]  # noqa: ARG002
    ) -> Err[E]:
        return self

    async def bind_async[T, U](
        self, f: Callable[[T], Awaitable[Ok[U] | Err[E]]]  # noqa: ARG002
    ) -> Err[E]:
        return self

    async def alt_async[F](
        self, f: Callable[[E], Awaitable[F]]
    ) -> Err[F]:
        """Transforma el error de forma asíncrona."""
        return Err(await f(self.error))

    async def lash_async[F](
        self, f: Callable[[E], Awaitable[Ok[F] | Err[F]]]
    ) -> Ok[F] | Err[F]:
        """Recuperación asíncrona desde error."""
        return await f(self.error)

    def __bool__(self) -> bool:
        return False


# ---------------------------------------------------------------------------
# Alias de tipo público
# ---------------------------------------------------------------------------

type Result[T, E] = Ok[T] | Err[E]


# ---------------------------------------------------------------------------
# Funciones estáticas de módulo (sin cambios)
# ---------------------------------------------------------------------------

def map2[T, U, V, E](
    r1: Ok[T] | Err[E],
    r2: Ok[U] | Err[E],
    f: Callable[[T, U], V],
) -> Ok[V] | Err[E]:
    match (r1, r2):
        case (Ok(value=a), Ok(value=b)):
            return Ok(f(a, b))
        case (Err() as e, _):
            return e
        case (_, Err() as e):
            return e
        case _:  # pragma: no cover
            raise TypeError(
                f"map2: tipos inesperados ({type(r1).__name__}, {type(r2).__name__})"
            )


def combine[T, E](
    results: list[Ok[T] | Err[E]],
) -> Ok[list[T]] | Err[E]:
    values: list[T] = []
    for r in results:
        match r:
            case Ok(value=v):
                values.append(v)
            case Err() as e:
                return e
    return Ok(values)


def from_exception[T, E: Exception](
    f: Callable[[], T],
    exc_type: type[E],
) -> Ok[T] | Err[E]:
    try:
        return Ok(f())
    except exc_type as e:
        return Err(e)  # type: ignore[return-value]


__all__ = [
    "Ok",
    "Err",
    "Result",
    "UnwrapError",
    "map2",
    "combine",
    "from_exception",
]