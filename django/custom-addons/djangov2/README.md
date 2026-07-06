# djangov2 - API CRUD con Django REST Framework + interfaz tipo tienda

Ruta solicitada:

```bash
ProgII_UTE202601/django/custom-addons/djangov2
```

## Instalacion rapida

```bash
cd ProgII_UTE202601/django/custom-addons/djangov2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_datos_demo
python manage.py runserver
```

## Interfaz visual tipo tienda

- `GET /` pagina principal con resumen del sistema.
- `GET /tienda/` catalogo visual de productos.
- `GET /categorias-panel/` panel de categorias.
- `GET /clientes-panel/` panel de clientes.
- `GET /pedidos-panel/` panel de pedidos y detalles.

La interfaz esta hecha con templates de Django, CSS personalizado y consultas a los 5 modelos del proyecto.

## Endpoints principales de API

- `GET/POST /api/categorias/`
- `GET/PUT/PATCH/DELETE /api/categorias/<id>/`
- `GET/POST /api/productos/`
- `GET/PUT/PATCH/DELETE /api/productos/<id>/`
- `GET/POST /api/clientes/`
- `GET/PUT/PATCH/DELETE /api/clientes/<id>/`
- `GET/POST /api/pedidos/`
- `GET/PUT/PATCH/DELETE /api/pedidos/<id>/`
- `GET/POST /api/detalles-pedido/`
- `GET/PUT/PATCH/DELETE /api/detalles-pedido/<id>/`

## Commit sugerido

```bash
git add django/custom-addons/djangov2
git commit -m "Agrega interfaz tipo tienda para djangov2"
git push origin main
```
