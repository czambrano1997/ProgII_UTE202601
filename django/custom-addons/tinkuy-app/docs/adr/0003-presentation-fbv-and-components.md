# ADR 0003 — Presentación: FBV y componentes de inclusión

**Estado:** Aceptado  
**Fecha:** 2025-06

## Contexto

Django ofrece vistas basadas en clase (CBV) y en función (FBV). Para la capa de
presentación, se necesita un sistema de componentes reutilizables sin añadir
dependencias pesadas.

## Decisión

- **Vistas basadas en función (FBV)**, tipadas con `HttpRequest → HttpResponse`.
- **Componentes** implementados como *inclusion tags* en
  `events/templatetags/components.py` + parciales en `templates/components/`.
- Cada componente tiene un comentario de contrato de props al inicio del parcial.
- Los componentes son **solo presentación**: reciben props, no hacen consultas.

La estructura está diseñada para migrar cada componente a `<c-x>` de
`django-cotton` o `django-components` en el futuro sin mover archivos (ADR 0003).

## Consecuencias

- Las vistas quedan cortas y legibles.
- Los componentes son testeables aisladamente.
- No se instala ningún framework de componentes en este sprint.
