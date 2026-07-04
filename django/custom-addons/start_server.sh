#!/bin/bash

# Script de inicio para Cancha Manager
# Ejecutar: bash start_server.sh

echo "🚀 Iniciando Cancha Manager..."
echo "================================"

# Verificar si estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py no encontrado. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

echo "✓ Directorio correcto encontrado"
echo ""

# Crear/actualizar migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate
echo ""

# Recopilar archivos estáticos
echo "🎨 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput
echo ""

# Iniciar servidor
echo "✅ ¡Servidor iniciado!"
echo ""
echo "📍 Accede a:"
echo "   - Web: http://127.0.0.1:8000/djangov1/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "⌨️  Presiona Ctrl+C para detener el servidor"
echo ""

python manage.py runserver
