# Proyecto: djangov1

Este documento describe la aplicación `djangov1` creada como parte del proyecto individual en Django.

Resumen:
- App: `djangov1` ubicada en `custom-addons/djangov1`.
- Modelos: `Categoria`, `Proveedor`, `Producto`, `Almacen`, `EntradaStock`.
- Cada modelo usa distintos campos de Django y hay relaciones: `ForeignKey` y `ManyToMany`.
- Vistas: List views para cada modelo en `custom-addons/djangov1/views.py`.
- Templates: en `custom-addons/djangov1/templates/djangov1/` (listas para cada modelo).
- Admin: todos los modelos están registrados en `custom-addons/djangov1/admin.py`.

Instrucciones para correr:
1. Activar el virtualenv del proyecto (si existe):
   ```bash
   source .venv/bin/activate
   ```
2. Instalar requisitos (si es necesario):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar migraciones (ya se aplicaron localmente):
   ```bash
   python manage.py migrate
   ```
4. Levantar servidor:
   ```bash
   python manage.py runserver 8000
   ```
5. Abrir las URLs de la app: `/djangov1/categorias/`, `/djangov1/productos/`, etc.

Descripción breve de los modelos:

- `Categoria`: `CharField`, `TextField`, `unique`.
- `Proveedor`: `CharField`, `EmailField`.
- `Producto`: `CharField`, `DecimalField`, `ForeignKey` a `Categoria`, `ManyToMany` a `Proveedor`.
- `Almacen`: `CharField` para ubicación.
- `EntradaStock`: `ForeignKey` a `Producto` y `Almacen`, `IntegerField`, `DateField`.

Último commit (local): se incluye la captura en el PDF generado.
