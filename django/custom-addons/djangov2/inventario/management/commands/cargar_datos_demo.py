from decimal import Decimal

from django.core.management.base import BaseCommand

from inventario.models import Categoria, Cliente, DetallePedido, Pedido, Producto


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para mostrar la interfaz tipo tienda.'

    def handle(self, *args, **options):
        tecnologia, _ = Categoria.objects.get_or_create(
            nombre='Tecnologia',
            defaults={'descripcion': 'Productos electronicos y accesorios.'}
        )
        ropa, _ = Categoria.objects.get_or_create(
            nombre='Ropa',
            defaults={'descripcion': 'Prendas y articulos de vestir.'}
        )
        hogar, _ = Categoria.objects.get_or_create(
            nombre='Hogar',
            defaults={'descripcion': 'Productos para casa y uso diario.'}
        )

        productos_demo = [
            (tecnologia, 'Audifonos Bluetooth', 'Audifonos inalambricos con buena bateria.', Decimal('24.99'), 18),
            (tecnologia, 'Mouse Gamer', 'Mouse ergonomico con luces LED.', Decimal('18.50'), 25),
            (tecnologia, 'Teclado Mecanico', 'Teclado compacto para estudio y trabajo.', Decimal('39.90'), 12),
            (ropa, 'Camiseta Basica', 'Camiseta comoda para uso diario.', Decimal('12.00'), 40),
            (ropa, 'Chompa Urbana', 'Chompa casual con diseno moderno.', Decimal('32.75'), 16),
            (hogar, 'Lampara LED', 'Lampara decorativa para escritorio.', Decimal('15.25'), 20),
            (hogar, 'Organizador', 'Caja organizadora multiuso.', Decimal('9.99'), 35),
        ]

        productos = []
        for categoria, nombre, descripcion, precio, stock in productos_demo:
            producto, _ = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria,
                    'descripcion': descripcion,
                    'precio': precio,
                    'stock': stock,
                    'activo': True,
                }
            )
            productos.append(producto)

        cliente, _ = Cliente.objects.get_or_create(
            cedula='1712345678',
            defaults={
                'nombres': 'Martin',
                'apellidos': 'Caza',
                'correo': 'martin.caza@example.com',
                'telefono': '0999999999',
            }
        )

        if not Pedido.objects.exists() and productos:
            pedido = Pedido.objects.create(cliente=cliente, estado='PAGADO')
            DetallePedido.objects.create(pedido=pedido, producto=productos[0], cantidad=1)
            DetallePedido.objects.create(pedido=pedido, producto=productos[3], cantidad=2)

        self.stdout.write(self.style.SUCCESS('Datos demo cargados correctamente.'))
