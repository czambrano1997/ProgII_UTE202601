# ADR 0002 — Tipado estricto: Pyright strict + django-types

**Estado:** Aceptado  
**Fecha:** 2025-06

## Contexto

Django no está tipado en su distribución oficial. Existen dos paquetes de stubs:
`django-stubs` (requiere el plugin de mypy) y `django-types` (funciona con
pyright sin plugin).

## Decisión

Usar **pyright en modo `strict`** con **`django-types`** (no `django-stubs`).

- `django-types` no requiere plugin y es compatible con pyright 1.1+.
- `typeCheckingMode = "strict"` en `pyproject.toml`.
- Las migraciones se excluyen (`exclude = ["**/migrations/**"]`) — son código
  generado y no necesitan tipado estricto.
- La anotación `id: int` se agrega explícitamente en los modelos que necesiten
  acceder al PK, porque django-types no infiere el campo implícito `id`.

## Consecuencias

- `uv run pyright` debe terminar con **0 errores** — es el gate de CI.
- No se usa `# type: ignore` excepto en el único punto de cruce con la API
  privada de Django (`cursor.execute` en `_sql.py`).
