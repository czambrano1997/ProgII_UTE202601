# djangov1

Aplicación Django para el proyecto individual con los siguientes componentes:

- 5 modelos: `Autor`, `CategoriaLibro`, `Libro`, `Cliente`, `Prestamo`
- Campos Django variados: `CharField`, `EmailField`, `URLField`, `TextField`, `BooleanField`, `DateField`, `DateTimeField`, `DecimalField`, `PositiveIntegerField`, `ForeignKey`, `ManyToManyField`
- Relaciones entre modelos:
  - `Libro` → `CategoriaLibro`
  - `Libro` ↔ `Autor`
  - `Prestamo` → `Cliente`
  - `Prestamo` → `Libro`
- Views y templates por cada modelo
- Admin configurado para los 5 modelos
- Ruta raíz y rutas de la app en `core/urls.py`

## Archivos clave

- `models.py`
- `views.py`
- `urls.py`
- `admin.py`
- `templates/djangov1/`
- `documentacion_djangov1.pdf`

## Instrucción de commit

Guardar los cambios y hacer commit desde la carpeta `custom-addons/djangov1`:

```bash
git add custom-addons/djangov1
git commit -m "Agrega app djangov1 con 5 modelos, vistas, templates y documentación PDF"
```
