# Documentación del proyecto djangov2

Resumen: se implementó una app `djangov2` con 5 modelos y API REST (CRUD) usando Django REST Framework.

Modelos implementados:
- `Category`: campos `name`, `description`.
- `Product`: FK `category`, `name`, `description`, `price`, `stock`, `created_at`.
- `Customer`: `first_name`, `last_name`, `email`, `phone`, `created_at`.
- `Order`: FK `customer`, `items` (JSON), `total`, `status`, `created_at`.
- `Review`: FK `product`, FK `customer` (opcional), `rating`, `comment`, `created_at`.

Endpoints (todos soportan GET, POST, PUT, PATCH, DELETE):
- `/api/categories/` - CRUD de categorías
- `/api/products/` - CRUD de productos
- `/api/customers/` - CRUD de clientes
- `/api/orders/` - CRUD de pedidos
- `/api/reviews/` - CRUD de reseñas

Pasos realizados:
1. Añadir `rest_framework` y `djangov2` en `progl1_ute202601/settings.py`.
2. Definir modelos en `djangov2/models.py`.
3. Crear serializers en `djangov2/serializers.py`.
4. Implementar viewsets en `djangov2/views.py`.
5. Registrar rutas en `djangov2/urls.py` e incluirlas en el proyecto (`/api/`).
6. Crear migraciones y aplicarlas (instrucciones abajo).

Cómo generar migraciones y ejecutar servidor:

```powershell
cd c:\Users\jandry\OneDrive\Desktop\djangoapi
.venv\Scripts\python.exe manage.py makemigrations
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Cómo generar el PDF final del informe (recomendado):
1. Convertir este `DOCUMENTACION.md` a PDF con una herramienta como `pandoc` o exportando desde un editor.
2. Adjuntar captura del último commit en el repositorio (hacer `git log -1 --stat` y capturar pantalla).

Métodos documentados por endpoint:
- GET / POST / PUT / PATCH / DELETE funcionan usando los `ViewSet` de DRF; los serializadores son `ModelSerializer`.

Conclusiones:
- Esta implementación ofrece una API básica y extensible para añadir validaciones, autenticación y pruebas.
