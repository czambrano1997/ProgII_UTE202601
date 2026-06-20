# Tinkuy

Plataforma de eventos universitarios — Django 5.2 + PostgreSQL + Tailwind CSS.

## Requisitos

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- PostgreSQL 15+

## Configuración inicial

```bash
cp .env.example .env
# edita .env con tus credenciales de Postgres

uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

## Tailwind CSS

Compilar una vez:

```bash
uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css
```

Modo watch (desarrollo):

```bash
uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css --watch
```

## Verificación de tipos

```bash
uv run pyright
```
