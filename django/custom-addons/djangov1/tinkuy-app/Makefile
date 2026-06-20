.PHONY: typecheck tailwind migrate superuser

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
