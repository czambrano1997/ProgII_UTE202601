# ADR 0004 — Estilos: Tailwind CSS (CLI standalone, sin Node)

**Estado:** Aceptado  
**Fecha:** 2025-06

## Contexto

El proyecto necesita un sistema de estilos moderno y utilitario. Node.js añade
complejidad al entorno de desarrollo Python.

## Decisión

Usar **Tailwind CSS** a través de `pytailwindcss` — el wrapper Python del binario
standalone de Tailwind (no requiere Node.js).

```bash
uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css
uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css --watch  # dev
```

El fichero compilado `static/css/tailwind.css` está en `.gitignore` y se
regenera en cada deploy. `tailwind.config.js` apunta a `./templates/**/*.html`.

## Consecuencias

- Sin Node, sin `npm install`, sin `package.json`.
- El binario de Tailwind se descarga automáticamente la primera vez vía `pytailwindcss`.
- Las clases no usadas se eliminan en la compilación (tree-shaking por contenido).
