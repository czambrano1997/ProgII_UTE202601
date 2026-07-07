# djangov2 API REST

Proyecto Django `djangov2` que expone CRUD completo sobre 5 modelos con Django REST Framework.

## Modelos implementados

- `Producto`
- `Cliente`
- `Categoria`
- `Pedido`
- `DetallePedido`

## Arquitectura y componentes

- `models.py`: definición de los 5 modelos del dominio.
- `serializers.py`: mapeo entre los modelos y JSON.
- `views.py`: `ModelViewSet` para cada modelo.
- `urls.py`: `DefaultRouter` para registrar rutas de API.
- `settings.py`: `rest_framework` agregado a `INSTALLED_APPS`.

## Endpoints disponibles

| Modelo | Lista | Detalle |
|---|---|---|
| Producto | `GET /api/productos/` | `GET /api/productos/{id}/` |
| Cliente | `GET /api/clientes/` | `GET /api/clientes/{id}/` |
| Categoria | `GET /api/categorias/` | `GET /api/categorias/{id}/` |
| Pedido | `GET /api/pedidos/` | `GET /api/pedidos/{id}/` |
| DetallePedido | `GET /api/detalle-pedidos/` | `GET /api/detalle-pedidos/{id}/` |

## Operaciones CRUD

- `GET` list: obtener todos los registros de un recurso.
- `GET` detail: obtener un registro por ID.
- `POST`: crear un nuevo registro.
- `PUT`: actualizar completamente un registro existente.
- `PATCH`: actualizar parcialmente un registro existente.
- `DELETE`: eliminar un registro.

### Ejemplo de uso para `Producto`

- Crear: `POST /api/productos/` con body JSON.
- Actualizar completo: `PUT /api/productos/1/`.
- Actualizar parcial: `PATCH /api/productos/1/`.
- Eliminar: `DELETE /api/productos/1/`.

## Pasos y configuraciones realizadas

1. Creación del proyecto Django `djangov2` en `custom-addons/djangov2`.
2. Creación de la app `tienda` en `custom-addons/djangov2/tienda`.
3. Configuración en `djangov2/settings.py`:
   - Agregado `rest_framework`.
   - Agregado `tienda`.
4. Definición de modelos en `tienda/models.py` para los 5 objetos.
5. Creación de serializadores en `tienda/serializers.py`.
6. Implementación de `ModelViewSet` en `tienda/views.py`.
7. Registro de rutas con `DefaultRouter` en `tienda/urls.py`.
8. Inclusión de `tienda.urls` en `djangov2/urls.py` bajo `api/`.
9. Ejecución de migraciones:
   - `python3 manage.py makemigrations tienda`
   - `python3 manage.py migrate`

## Métodos implementados

- `GET /api/<recurso>/`: listado completo del recurso.
- `GET /api/<recurso>/{id}/`: detalle del recurso.
- `POST /api/<recurso>/`: creación de nuevo recurso.
- `PUT /api/<recurso>/{id}/`: reemplazo completo de recurso.
- `PATCH /api/<recurso>/{id}/`: actualización parcial de recurso.
- `DELETE /api/<recurso>/{id}/`: eliminación del recurso.

## Conclusiones

Se completó la exposición de una API REST para 5 modelos del proyecto usando Django REST Framework. La solución utiliza `ModelViewSet` para simplificar la implementación del CRUD y `DefaultRouter` para generar automáticamente las rutas necesarias.

La arquitectura queda lista para extenderse con autenticación, permisos y validaciones adicionales.
