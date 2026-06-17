# DjangoV1 - Sistema de inventario y ventas

Proyecto individual para Programación II. La aplicación reemplaza la temática académica por un catálogo de productos, proveedores, clientes y pedidos.

## Modelos

La aplicación contiene seis modelos:

1. `Categoria`
2. `Proveedor`
3. `Producto`
4. `Cliente`
5. `Pedido`
6. `DetallePedido`

`Producto` se relaciona con `Categoria` y `Proveedor` mediante `ForeignKey`. `Pedido` se relaciona con `Cliente` mediante `ForeignKey`. La relación muchos a muchos entre `Pedido` y `Producto` utiliza el modelo intermedio `DetallePedido`.

## Requisitos

- Python 3.10 o superior.
- Acceso a Internet durante la instalación de dependencias.
- Linux con el paquete `python3-venv` instalado.

En Ubuntu/Debian, si `venv` no está disponible:

```bash
sudo apt update
sudo apt install python3-venv
```

## Instalación automática

Ubícate en esta carpeta y ejecuta:

```bash
chmod +x preparar_proyecto.sh
./preparar_proyecto.sh
```

El script crea `.venv`, instala Django, aplica migraciones, carga datos demo y ejecuta las pruebas.

## Instalación manual

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_datos_demo
python manage.py preparar_admin_emily
python manage.py check
python manage.py test djangov1.tests -v 2
python manage.py preparar_admin_emily
python manage.py changepassword emily
python manage.py runserver
```

No se incluye ninguna contraseña. El comando `preparar_admin_emily` crea o prepara el usuario `emily` como administrador sin establecer una contraseña visible. Después debes asignarla de forma interactiva:

```bash
python manage.py changepassword emily
```

## Rutas

- `/`
- `/categorias/`
- `/proveedores/`
- `/productos/`
- `/clientes/`
- `/pedidos/`
- `/detalles-pedido/`
- `/admin/`

## Git

Antes de confirmar cambios:

```bash
cd ~/ProgII_UTE202601
git branch --show-current
git status
```

La rama debe ser:

```text
estudiante/emily_torres
```

Comandos sugeridos:

```bash
git add django/custom-addons/djangov1 .gitignore
git commit -m "feat: implementar sistema de inventario y ventas en Django"
git push origin estudiante/emily_torres
```

Después del `push`, toma una captura de GitHub mostrando el repositorio, la rama, la ruta del proyecto y el último commit. Sustituye la página pendiente del informe editable y vuelve a exportarlo a PDF.
