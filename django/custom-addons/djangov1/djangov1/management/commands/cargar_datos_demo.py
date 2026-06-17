from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from djangov1.models import Categoria, Cliente, DetallePedido, Pedido, Producto, Proveedor


class Command(BaseCommand):
    help = "Crea o actualiza un conjunto de datos de demostración. Es seguro ejecutarlo varias veces."

    @transaction.atomic
    def handle(self, *args, **options):
        categorias = {}
        for datos in [
            {"nombre": "Tecnología", "slug": "tecnologia", "descripcion": "Equipos y accesorios tecnológicos."},
            {"nombre": "Oficina", "slug": "oficina", "descripcion": "Artículos para trabajo y estudio."},
            {"nombre": "Hogar", "slug": "hogar", "descripcion": "Productos de uso doméstico."},
        ]:
            categoria, _ = Categoria.objects.update_or_create(slug=datos["slug"], defaults=datos)
            categorias[datos["slug"]] = categoria

        proveedores = {}
        for datos in [
            {
                "nombre": "Distribuidora Andina",
                "correo": "ventas@andina.example",
                "telefono": "0991112233",
                "sitio_web": "https://example.com/andina",
                "activo": True,
            },
            {
                "nombre": "Comercial Pacífico",
                "correo": "pedidos@pacifico.example",
                "telefono": "0984445566",
                "sitio_web": "https://example.com/pacifico",
                "activo": True,
            },
        ]:
            proveedor, _ = Proveedor.objects.update_or_create(correo=datos["correo"], defaults=datos)
            proveedores[datos["correo"]] = proveedor

        productos_datos = [
            {
                "sku": "TEC-001",
                "nombre": "Teclado mecánico",
                "slug": "teclado-mecanico",
                "descripcion": "Teclado USB con iluminación.",
                "categoria": categorias["tecnologia"],
                "proveedor": proveedores["ventas@andina.example"],
                "precio": Decimal("49.90"),
                "stock": 12,
                "stock_minimo": 4,
            },
            {
                "sku": "TEC-002",
                "nombre": "Mouse inalámbrico",
                "slug": "mouse-inalambrico",
                "descripcion": "Mouse ergonómico con receptor USB.",
                "categoria": categorias["tecnologia"],
                "proveedor": proveedores["ventas@andina.example"],
                "precio": Decimal("18.50"),
                "stock": 3,
                "stock_minimo": 5,
            },
            {
                "sku": "OFI-001",
                "nombre": "Cuaderno universitario",
                "slug": "cuaderno-universitario",
                "descripcion": "Cuaderno de 100 hojas cuadriculadas.",
                "categoria": categorias["oficina"],
                "proveedor": proveedores["pedidos@pacifico.example"],
                "precio": Decimal("3.75"),
                "stock": 40,
                "stock_minimo": 10,
            },
            {
                "sku": "OFI-002",
                "nombre": "Organizador de escritorio",
                "slug": "organizador-escritorio",
                "descripcion": "Organizador modular para útiles.",
                "categoria": categorias["oficina"],
                "proveedor": proveedores["pedidos@pacifico.example"],
                "precio": Decimal("11.20"),
                "stock": 9,
                "stock_minimo": 3,
            },
            {
                "sku": "HOG-001",
                "nombre": "Lámpara LED",
                "slug": "lampara-led",
                "descripcion": "Lámpara de escritorio con brazo ajustable.",
                "categoria": categorias["hogar"],
                "proveedor": proveedores["ventas@andina.example"],
                "precio": Decimal("24.00"),
                "stock": 7,
                "stock_minimo": 2,
            },
        ]

        productos = {}
        for datos in productos_datos:
            sku = datos.pop("sku")
            producto, _ = Producto.objects.update_or_create(sku=sku, defaults=datos)
            productos[sku] = producto

        clientes = {}
        for datos in [
            {
                "nombres": "María",
                "apellidos": "López",
                "correo": "maria.lopez@example.com",
                "telefono": "0992223344",
                "direccion": "Quito, Ecuador",
                "fecha_nacimiento": date(1998, 5, 14),
                "activo": True,
            },
            {
                "nombres": "Carlos",
                "apellidos": "Mendoza",
                "correo": "carlos.mendoza@example.com",
                "telefono": "0985556677",
                "direccion": "Guayaquil, Ecuador",
                "fecha_nacimiento": date(1995, 10, 2),
                "activo": True,
            },
        ]:
            cliente, _ = Cliente.objects.update_or_create(correo=datos["correo"], defaults=datos)
            clientes[datos["correo"]] = cliente

        pedidos = [
            {
                "codigo": "PED-0001",
                "cliente": clientes["maria.lopez@example.com"],
                "estado": Pedido.Estado.PAGADO,
                "observaciones": "Retiro en tienda.",
                "entregado": False,
                "detalles": [
                    (productos["TEC-001"], 1, Decimal("49.90"), Decimal("0")),
                    (productos["OFI-001"], 3, Decimal("3.75"), Decimal("5")),
                ],
            },
            {
                "codigo": "PED-0002",
                "cliente": clientes["carlos.mendoza@example.com"],
                "estado": Pedido.Estado.ENVIADO,
                "observaciones": "Entrega en horario de oficina.",
                "entregado": False,
                "detalles": [
                    (productos["TEC-002"], 2, Decimal("18.50"), Decimal("0")),
                    (productos["HOG-001"], 1, Decimal("24.00"), Decimal("10")),
                ],
            },
        ]

        for datos in pedidos:
            detalles = datos.pop("detalles")
            pedido, _ = Pedido.objects.update_or_create(codigo=datos["codigo"], defaults=datos)
            for producto, cantidad, precio, descuento in detalles:
                DetallePedido.objects.update_or_create(
                    pedido=pedido,
                    producto=producto,
                    defaults={
                        "cantidad": cantidad,
                        "precio_unitario": precio,
                        "descuento": descuento,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados correctamente."))
