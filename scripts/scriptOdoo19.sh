#!/bin/bash

# -----------------------------------------------------------------------------
# Script de instalación automática de Odoo 19 en Ubuntu 24.04
# -----------------------------------------------------------------------------
# Este script debe ejecutarse con privilegios de superusuario (sudo)
# pero realiza la mayor parte de la configuración con el usuario original.
# -----------------------------------------------------------------------------

set -e  # Detener el script si ocurre algún error

# Función para mostrar mensajes en color
info() {
    echo -e "\n\033[1;34m[INFO]\033[0m $1"
}

error() {
    echo -e "\n\033[1;31m[ERROR]\033[0m $1" >&2
    exit 1
}

# Verificar que el script se ejecuta con sudo
if [ "$EUID" -ne 0 ]; then
    error "Este script debe ejecutarse con sudo. Usa: sudo $0"
fi

# Detectar el usuario que invocó sudo (el usuario real)
if [ -z "$SUDO_USER" ]; then
    error "No se pudo determinar el usuario original. Asegúrate de ejecutar con sudo, no como root directo."
fi
REAL_USER="$SUDO_USER"
REAL_HOME=$(eval echo "~$REAL_USER")

info "Usuario real detectado: $REAL_USER"

# -----------------------------------------------------------------------------
# 1. Solicitar datos al usuario (ejecutado como root pero guardamos variables)
# -----------------------------------------------------------------------------
echo "================================================================="
echo "   CONFIGURACIÓN DE ODOO 19 EN UBUNTU 24.04"
echo "================================================================="
read -p "Directorio de trabajo (ej. /home/$REAL_USER/ProyectoOdoo): " WORK_DIR
read -p "Nombre de usuario para PostgreSQL: " DB_USER
read -s -p "Contraseña para el usuario PostgreSQL: " DB_PASSWORD
echo
read -s -p "Contraseña de administrador de Odoo (admin_passwd): " ADMIN_PASSWD
echo

# Validar entradas básicas
if [ -z "$WORK_DIR" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$ADMIN_PASSWD" ]; then
    error "Todos los campos son obligatorios."
fi

# -----------------------------------------------------------------------------
# 2. Instalar paquetes del sistema (como root)
# -----------------------------------------------------------------------------
info "Actualizando repositorios e instalando paquetes del sistema..."
apt update --fix-missing
apt install -y postgresql python3-venv python3-pip unzip \
#    build-essential libpq-dev libxml2-dev libxslt1-dev \
#    libldap2-dev libsasl2-dev libssl-dev libjpeg-dev zlib1g-dev \
#    libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
#    libfribidi-dev libxcb1-dev libxcb-render0-dev libxcb-shm0-dev \
#    libxcb-xfixes0-dev

# -----------------------------------------------------------------------------
# 3. Configurar PostgreSQL (como root y usuario postgres)
# -----------------------------------------------------------------------------
info "Configurando PostgreSQL..."

# Obtener versión de PostgreSQL instalada (por defecto 16 en Ubuntu 24.04)
PG_VERSION=$(psql --version | awk '{print $NF}' | cut -d. -f1)
PG_CONF_DIR="/etc/postgresql/$PG_VERSION/main"
if [ ! -d "$PG_CONF_DIR" ]; then
    error "No se encontró el directorio de configuración de PostgreSQL $PG_CONF_DIR"
fi

# Crear usuario en PostgreSQL
info "Creando usuario $DB_USER en PostgreSQL..."
sudo -u postgres psql -c "CREATE USER $DB_USER;" 2>/dev/null || true
sudo -u postgres psql -c "ALTER ROLE $DB_USER WITH SUPERUSER CREATEDB;" || error "No se pudo asignar roles a $DB_USER"
sudo -u postgres psql -c "ALTER ROLE $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';" || error "No se pudo establecer contraseña para $DB_USER"

# Modificar postgresql.conf
info "Modificando $PG_CONF_DIR/postgresql.conf..."
sed -i "s/^#listen_addresses = .*/listen_addresses = '*'/" "$PG_CONF_DIR/postgresql.conf"
if ! grep -q "^listen_addresses = '\*'" "$PG_CONF_DIR/postgresql.conf"; then
    echo "listen_addresses = '*'" >> "$PG_CONF_DIR/postgresql.conf"
fi

# Modificar pg_hba.conf
info "Modificando $PG_CONF_DIR/pg_hba.conf..."
HBA_LINE="local   all             $DB_USER                                md5"
if ! grep -q "$HBA_LINE" "$PG_CONF_DIR/pg_hba.conf"; then
    echo "$HBA_LINE" >> "$PG_CONF_DIR/pg_hba.conf"
fi

# Reiniciar PostgreSQL
info "Reiniciando servicio PostgreSQL..."
systemctl restart postgresql || error "No se pudo reiniciar PostgreSQL"

# -----------------------------------------------------------------------------
# 4. Tareas como usuario real (sin privilegios)
# -----------------------------------------------------------------------------
# A partir de aquí, los comandos se ejecutarán con el usuario original usando sudo -u
run_as_user() {
    sudo -u "$REAL_USER" bash -c "$1"
}

# Crear directorio de trabajo si no existe, con permisos para el usuario real
if [ ! -d "$WORK_DIR" ]; then
    info "Creando directorio de trabajo: $WORK_DIR"
    run_as_user "mkdir -p '$WORK_DIR'"
else
    # Asegurar que el directorio pertenezca al usuario real
    chown -R "$REAL_USER:$REAL_USER" "$WORK_DIR"
fi

# Verificar existencia del archivo zip
ZIP_FILE="$WORK_DIR/odoo-19.0.zip"
if [ ! -f "$ZIP_FILE" ]; then
    error "No se encontró el archivo odoo-19.0.zip en $WORK_DIR. Colócalo manualmente y vuelve a ejecutar el script."
fi

# Descomprimir como usuario real
info "Descomprimiendo odoo-19.0.zip..."
run_as_user "cd '$WORK_DIR' && unzip -q 'odoo-19.0.zip'"
ODIR="$WORK_DIR/odoo-19.0"
if [ ! -d "$ODIR" ]; then
    error "No se encontró el directorio odoo-19.0 después de descomprimir."
fi

# Crear entorno virtual Python como usuario real
info "Creando entorno virtual de Python (.venv)..."
run_as_user "cd '$WORK_DIR' && python3 -m venv .venv"

# Preparar requirements.txt e instalar dependencias Python
info "Modificando requirements.txt (comentando psycopg2 y python-ldap)..."
REQ_FILE="$ODIR/requirements.txt"
if [ ! -f "$REQ_FILE" ]; then
    error "No se encontró requirements.txt en $ODIR"
fi

# Hacer copia de seguridad y modificar
run_as_user "cp '$REQ_FILE' '$REQ_FILE.bak'"
run_as_user "sed -i '/psycopg2/s/^#*/#/' '$REQ_FILE'"
run_as_user "sed -i '/python-ldap/s/^#*/#/' '$REQ_FILE'"

info "Instalando paquetes desde requirements.txt (puede tardar unos minutos)..."
run_as_user "source '$WORK_DIR/.venv/bin/activate' && pip install --upgrade pip wheel setuptools"
run_as_user "source '$WORK_DIR/.venv/bin/activate' && pip install -r '$REQ_FILE'"

info "Instalando psycopg2-binary y python3-ldap..."
run_as_user "source '$WORK_DIR/.venv/bin/activate' && pip install psycopg2-binary python3-ldap"

# Crear directorio custom-addons
info "Creando directorio custom-addons..."
CUSTOM_ADDONS_DIR="$WORK_DIR/custom-addons"
run_as_user "mkdir -p '$CUSTOM_ADDONS_DIR'"

# Determinar rutas estándar de addons de Odoo 19
ODOO_ADDONS_PATH="$ODIR/odoo/addons"
ADDONS_PATH="$ODIR/addons"

# Configurar archivo odoo.conf como usuario real
info "Copiando y configurando odoo.conf..."
OD_CONF_SRC="$ODIR/debian/odoo.conf"
OD_CONF_DST="$WORK_DIR/odoo.conf"

if [ ! -f "$OD_CONF_SRC" ]; then
    error "No se encontró $OD_CONF_SRC"
fi

run_as_user "cp '$OD_CONF_SRC' '$OD_CONF_DST'"

# Construir la línea de addons_path
ADDONS_PATH_LINE="addons_path = $ODOO_ADDONS_PATH,$ADDONS_PATH,$CUSTOM_ADDONS_DIR"

# Crear contenido de odoo.conf con las variables
run_as_user "cat > '$OD_CONF_DST' << EOF
[options]
; This is the password that allows database operations:
admin_passwd = $ADMIN_PASSWD
db_host = localhost
db_port = 5432
db_user = $DB_USER
db_password = $DB_PASSWORD
$ADDONS_PATH_LINE
; Si usas proxy
; proxy_mode = True
; Log settings
;logfile = $WORK_DIR/odoo.log
log_level = info
EOF"

# Ajustar permisos finales
chown -R "$REAL_USER:$REAL_USER" "$WORK_DIR"

# -----------------------------------------------------------------------------
# 5. Finalización
# -----------------------------------------------------------------------------
info "¡Configuración completada con éxito!"
echo "================================================================="
echo "  Odoo 19 ha sido configurado en: $WORK_DIR"
echo "  Usuario PostgreSQL: $DB_USER"
echo "  Contraseña PostgreSQL: $DB_PASSWORD"
echo "  Contraseña admin Odoo: $ADMIN_PASSWD"
echo "  Directorio para módulos personalizados: $CUSTOM_ADDONS_DIR"
echo ""
echo "  Para iniciar Odoo, ejecuta (como usuario $REAL_USER):"
echo "    cd $WORK_DIR"
echo "    source .venv/bin/activate"
echo "    ./odoo-19.0/odoo-bin -c odoo.conf"
echo "================================================================="
