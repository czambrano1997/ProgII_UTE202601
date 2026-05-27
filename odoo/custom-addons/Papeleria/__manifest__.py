# -*- coding: utf-8 -*-
{
    'name': 'Papelería',
    'version': '19.0.1.0.0',
    'summary': 'Gestión de ventas para papelería',
    'description': """
        Módulo para la gestión integral de una papelería:
        - Productos con stock mínimo
        - Clientes y Proveedores
        - Categorías de productos
        - Ventas con líneas de detalle
    """,
    'author': 'Mi Empresa',
    'category': 'Sales',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/producto.xml',
        'views/cliente.xml',
        'views/proveedor.xml',
        'views/venta.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
