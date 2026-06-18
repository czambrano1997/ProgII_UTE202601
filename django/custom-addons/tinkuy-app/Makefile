.PHONY: check typecheck test tailwind migrate superuser

## Verificación completa (CI gate)
check: typecheck test

## Tipado estricto
typecheck:
	uv run pyright

## Tests (requiere Postgres corriendo con credenciales de .env)
test:
	uv run pytest tests/ -v

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
