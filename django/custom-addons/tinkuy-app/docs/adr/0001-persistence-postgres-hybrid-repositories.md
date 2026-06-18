# ADR 0001 — Persistencia: PostgreSQL con repositorios híbridos

**Estado:** Aceptado  
**Fecha:** 2025-06

## Contexto

La aplicación necesita acceso a la base de datos de forma predecible y testeable.
Django ORM es conveniente para escrituras y lecturas simples, pero para reportes
con JOINs complejos o agregaciones el ORM genera consultas difíciles de controlar.

## Decisión

Usar un **patrón repositorio híbrido**:

- **ORM de Django** para escrituras y lecturas simples → retorna instancias de
  modelo o `QuerySet[Model]`.
- **SQL crudo parametrizado** (`%s`, nunca f-strings ni `.format`) para reportes
  con JOINs y GROUP BY → retorna *frozen dataclass* DTOs tipados.

Un módulo por agregado en `events/repositories/`: `event_repository.py`,
`session_repository.py`, `attendee_repository.py`, `registration_repository.py`,
`speaker_repository.py`, `room_repository.py`.

El helper `_sql.fetchall` centraliza la ejecución de SQL crudo y la conversión de
filas a `dict[str, Any]`. El `Any` se detiene en la frontera del repositorio.

**Las vistas nunca importan modelos ni tocan el ORM directamente.**

## Consecuencias

- Inyección SQL imposible mientras se use `%s`.
- Los repositorios son el único lugar donde se escribe SQL.
- Los DTOs frozen son inmutables y seguros para pasar entre capas.
