#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no está instalado."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py preparar_admin_emily
python manage.py check
python manage.py test djangov1.tests -v 2

echo
echo "Proyecto preparado correctamente."
echo "Define la contraseña de emily con: python manage.py changepassword emily"
echo "Inicia el servidor con: python manage.py runserver"
