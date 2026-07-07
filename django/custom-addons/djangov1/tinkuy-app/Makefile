.PHONY: typecheck tailwind tailwind-watch migrate superuser run seed seed-flush test

## uv no carga .env por sí solo; esto lo inyecta en todos los `uv run`
## (solo si el archivo existe, para no romper targets sin .env)
export UV_ENV_FILE := $(wildcard .env)

## Tipado estricto (CI gate)
typecheck:
	uv run pyright

## Compilar Tailwind CSS
tailwind:
	uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css

## Modo watch Tailwind (desarrollo)
tailwind-watch:
	uv run tailwindcss -i static/src/input.css -o static/css/tailwind.css --watch

## Aplicar migraciones
migrate:
	uv run python manage.py migrate

## Crear superusuario
superuser:
	uv run python manage.py createsuperuser

## Servidor de desarrollo
run:
	uv run python manage.py runserver

## Sembrar datos de demostración (idempotente, vía repositorios)
seed:
	uv run python manage.py seed_demo --scale 8

## Sembrar desde cero (vacía los siete agregados primero)
seed-flush:
	uv run python manage.py seed_demo --flush --scale 8

## Pruebas (smoke de seeding + API end-to-end + repositorios)
test:
	uv run pytest
