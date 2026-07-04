# djangov2 API

Este archivo documenta la implementación de endpoints REST para los modelos seleccionados.

Modelos expuestos (endpoints CRUD):
- `Cliente` -> `/djangov2/clientes/`
- `Reserva` -> `/djangov2/reservas/`
- `Paquete` -> `/djangov2/paquetes/`
- `Inventario` -> `/djangov2/inventario/`
- `Canchas` -> `/djangov2/canchas/`

Cada ruta soporta los métodos HTTP estándar del CRUD:
- GET (lista y detalle): Obtener recursos.
- POST: Crear recurso.
- PUT: Reemplazar recurso completo.
- PATCH: Modificar parcial.
- DELETE: Eliminar recurso.

Pasos y configuraciones realizadas
1. Añadido `rest_framework` y `djangov2` a `INSTALLED_APPS` en `core/settings.py`.
2. Registrado `djangov2` en `core/urls.py` en la ruta `/djangov2/`.
3. Creado `djangov2/serializers.py` con `ModelSerializer` para los modelos.
4. Creado `djangov2/api_views.py` con `ModelViewSet` para cada modelo.
5. Registrado los viewsets con un `DefaultRouter` y agregado a `djangov2/urls.py`.

Ejemplos de uso
- Listar clientes:
  GET /djangov2/clientes/

- Crear cliente:
  POST /djangov2/clientes/
  Payload JSON:
  {
    "nombre": "Juan",
    "apellido": "Perez",
    "email": "juan@example.com",
    "telefono": "099999999"
  }

- Obtener detalle de cliente (id 1):
  GET /djangov2/clientes/1/

- Actualizar totalmente (PUT):
  PUT /djangov2/clientes/1/
  Payload: objeto completo

- Actualizar parcialmente (PATCH):
  PATCH /djangov2/clientes/1/
  Payload: {"telefono":"011111111"}

- Eliminar (DELETE):
  DELETE /djangov2/clientes/1/

Notas
- Permisos: por simplicidad los viewsets usan `AllowAny`.
- Validaciones: se usan las validaciones del `ModelSerializer` y los campos `unique` del modelo.

Conclusiones
- Se dispone de un API REST completo para los modelos principales.
- En producción, añadir autenticación, permisos y paginación.
- Considerar versionado (`/api/v1/`) y tests automatizados.
