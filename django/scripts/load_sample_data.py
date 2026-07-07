import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

django.setup()

from djangov1.models import Categoria, Proveedor, Producto, Almacen, EntradaStock

# Limpia datos existentes (solo para entorno de pruebas)
Categoria.objects.all().delete()
Proveedor.objects.all().delete()
Producto.objects.all().delete()
Almacen.objects.all().delete()
EntradaStock.objects.all().delete()

# Categorías
cats = [
    {'codigo':'CAT01','nombre':'Portátiles','descripcion':'Laptops y Ultrabooks'},
    {'codigo':'CAT02','nombre':'Smartphones','descripcion':'Teléfonos inteligentes'},
    {'codigo':'CAT03','nombre':'Periféricos','descripcion':'Teclados, ratones, auriculares'}
]
for c in cats:
    Categoria.objects.create(**c)

# Proveedores
provs = [
    {'nombre':'TechDistrib','email':'ventas@techdistrib.com','telefono':'099100200'},
    {'nombre':'GadgetsCo','email':'contacto@gadgetsco.com','telefono':'099200300'},
    {'nombre':'Electronix','email':'info@electronix.com','telefono':'099300400'},
]
for p in provs:
    Proveedor.objects.create(**p)

# Almacenes
alms = [
    {'nombre':'Almacén Central','direccion':'Av. Principal 123'},
    {'nombre':'Sucursal Norte','direccion':'Calle Norte 45'},
    {'nombre':'Sucursal Sur','direccion':'Calle Sur 67'},
]
for a in alms:
    Almacen.objects.create(**a)

# Productos (asignar categorías y proveedores)
cat_objs = list(Categoria.objects.all())
prov_objs = list(Proveedor.objects.all())
prod_defs = [
    {'sku':'LT100','nombre':'Laptop Pro 14','categoria':cat_objs[0],'descripcion':'Laptop 14" i7 16GB','precio':'1299.99'},
    {'sku':'SP200','nombre':'Smartphone X','categoria':cat_objs[1],'descripcion':'Smartphone 6.5" OLED','precio':'799.00'},
    {'sku':'PF300','nombre':'Teclado Mecánico K100','categoria':cat_objs[2],'descripcion':'Switch rojo, retroiluminado','precio':'99.50'},
]
for pd in prod_defs:
    proveedores = [prov_objs[0]]
    prod = Producto.objects.create(sku=pd['sku'], nombre=pd['nombre'], categoria=pd['categoria'], descripcion=pd['descripcion'], precio=pd['precio'])
    prod.proveedores.set(proveedores)

# Entradas de stock
alm_objs = list(Almacen.objects.all())
prod_objs = list(Producto.objects.all())
entries = [
    {'producto':prod_objs[0],'almacen':alm_objs[0],'cantidad':10},
    {'producto':prod_objs[1],'almacen':alm_objs[1],'cantidad':25},
    {'producto':prod_objs[2],'almacen':alm_objs[2],'cantidad':50},
]
for e in entries:
    EntradaStock.objects.create(producto=e['producto'], almacen=e['almacen'], cantidad=e['cantidad'])

print('Datos de ejemplo cargados correctamente.')
