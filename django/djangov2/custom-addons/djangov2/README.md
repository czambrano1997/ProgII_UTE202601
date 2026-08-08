# Django REST Framework API - Inventario

## Objetivo
Implementar la exposición CRUD de los modelos principales del proyecto Django MVT mediante Django REST Framework (DRF) y documentar los pasos, métodos y conclusiones.

## Pasos realizados
1. Instalar Django REST Framework en el entorno virtual del proyecto.
2. Agregar `rest_framework` a la configuración de `INSTALLED_APPS`.
3. Configurar la base de datos local en SQLite para facilitar pruebas y desarrollo.
4. Crear los serializadores para los modelos de Category, Supplier, Product, InventoryItem, Order y OrderItem.
5. Crear los viewsets basados en `ModelViewSet` para cada modelo.
6. Registrar los endpoints con `DefaultRouter` en `inventario/api_urls.py`.
7. Incluir las rutas de API en `core/urls.py`.
8. Crear pruebas de API para validar CRUD sobre los modelos principales.

## Endpoints implementados
- `GET /api/categories/` y `GET /api/categories/<id>/`
- `POST /api/categories/`
- `PUT /api/categories/<id>/`
- `PATCH /api/categories/<id>/`
- `DELETE /api/categories/<id>/`
- `GET /api/suppliers/`, `POST /api/suppliers/`, `GET /api/suppliers/<id>/`, `PUT /api/suppliers/<id>/`, `PATCH /api/suppliers/<id>/`, `DELETE /api/suppliers/<id>/`
- `GET /api/products/`, `POST /api/products/`, `GET /api/products/<id>/`, `PUT /api/products/<id>/`, `PATCH /api/products/<id>/`, `DELETE /api/products/<id>/`
- `GET /api/inventory-items/`, `POST /api/inventory-items/`, `GET /api/inventory-items/<id>/`, `PUT /api/inventory-items/<id>/`, `PATCH /api/inventory-items/<id>/`, `DELETE /api/inventory-items/<id>/`
- `GET /api/orders/`, `POST /api/orders/`, `GET /api/orders/<id>/`, `PUT /api/orders/<id>/`, `PATCH /api/orders/<id>/`, `DELETE /api/orders/<id>/`
- `GET /api/order-items/`, `POST /api/order-items/`, `GET /api/order-items/<id>/`, `PUT /api/order-items/<id>/`, `PATCH /api/order-items/<id>/`, `DELETE /api/order-items/<id>/`

## Métodos realizados
- `GET`: consulta de listas o recursos concretos.
- `POST`: creación de registros.
- `PUT`: actualización completa del registro.
- `PATCH`: actualización parcial del registro.
- `DELETE`: eliminación de un recurso.

## Conclusiones
La implementación con DRF permitió exponer de forma rápida y consistente los modelos del proyecto, facilitando la integración con clientes web o móviles y manteniendo una estructura clara basada en serializadores, viewsets y rutas.

## Verificación
Se ejecutó:

```bash
python manage.py test inventario.tests_api
```

Resultado: 5 pruebas aprobadas.
