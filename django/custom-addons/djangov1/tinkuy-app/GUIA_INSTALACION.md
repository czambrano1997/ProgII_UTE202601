# Tinkuy — Guía de instalación desde cero

Pasos para correr el API en una máquina nueva, con entorno virtual (`.venv`) propio, usuario de PostgreSQL propio y base de datos vacía. Tiempo estimado: 10 minutos.

## 1. Requisitos

- Python 3.13 recomendado (funciona con 3.11+)
- PostgreSQL 15+ corriendo localmente
- Un entorno virtual `.venv` en la carpeta del proyecto (`tinkuy-app/`):

```bash
python -m venv .venv

# activar — macOS / Linux:
source .venv/bin/activate
# activar — Windows (PowerShell):
.venv\Scripts\activate
```

Todos los comandos siguientes asumen el `.venv` activado.

## 2. Crear usuario y base de datos en PostgreSQL

Conéctate como administrador (`psql -U postgres`) y ejecuta, reemplazando usuario y contraseña por los tuyos:

```sql
CREATE USER mi_usuario WITH PASSWORD 'mi_password';
CREATE DATABASE tinkuy OWNER mi_usuario;
```

Ser dueño (OWNER) de la base es suficiente; no se necesitan permisos adicionales.

## 3. Configurar variables de entorno

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

Edita `.env` con las credenciales del paso 2:

```
POSTGRES_DB=tinkuy
POSTGRES_USER=mi_usuario
POSTGRES_PASSWORD=mi_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

El proyecto lee `.env` automáticamente (desde `tinkuy/settings.py`); no hace falta exportar nada.

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Instala Django 5.2, Django REST Framework y psycopg con versiones exactas.

## 5. Migrar la base de datos

```bash
python manage.py migrate
```

Crea todas las tablas y siembra la configuración inicial del sitio. La base queda lista aunque esté vacía de datos.

## 6. Crear tu superusuario (para /admin)

```bash
python manage.py createsuperuser
```

## 7. Levantar el servidor

```bash
python manage.py runserver
```

## 8. Probar

| URL | Qué es |
|---|---|
| http://127.0.0.1:8000/api/ | Raíz del API (lista los 6 recursos) |
| http://127.0.0.1:8000/api/events/ | CRUD de eventos (igual: rooms, speakers, sessions, attendees, registrations) |
| http://127.0.0.1:8000/admin/ | Django admin (con el superusuario del paso 6) |

El API es navegable desde el browser (DRF Browsable API) y no requiere autenticación (decisión de diseño para la demo, ADR-0006). Ejemplo por terminal:

```bash
curl http://127.0.0.1:8000/api/events/

curl -X POST http://127.0.0.1:8000/api/rooms/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Aula Magna","floor":1,"seating_capacity":100,"has_projector":true,"notes":""}'
```

## Opcional

**Datos de demostración** (requiere las dependencias de desarrollo; es idempotente, se puede repetir):

```bash
pip install -r requirements-dev.txt
python manage.py seed_demo --scale 8
```

**CSS de la interfaz web:** el repo no incluye el CSS compilado. El API y el admin funcionan sin esto; solo hace falta para ver las páginas web con estilos:

```bash
pip install -r requirements-dev.txt
tailwindcss -i static/src/input.css -o static/css/tailwind.css
```

**Si usas [uv](https://github.com/astral-sh/uv)** en lugar de venv+pip: `uv sync` instala todo (incluido Python 3.13) y cada comando se corre con `uv run python manage.py ...` o con los targets del Makefile (`make migrate`, `make run`, `make seed`).

## Problemas comunes

- `password authentication failed`: las credenciales de `.env` no coinciden con las creadas en el paso 2.
- `connection refused`: PostgreSQL no está corriendo (revisa el servicio del sistema).
- `port already in use`: usa otro puerto, p. ej. `python manage.py runserver 8001`.
- `No module named django`: el `.venv` no está activado o falta el paso 4.
