# -*- coding: utf-8 -*-
{
    "name": "Proyecto ",
    "version": "19.0.1.0.0",
    "category": "Tools",
    "summary": "Gestion de una empresa de prodcutos plasticos",
    "description": """"
        Módulo para administrar una empresa de productos plásticos.
        Incluye gestión de materiales, productos, órdenes de producción,
        control de calidad y pedidos de clientes.
        """,
    "author": 'PLASTIVENTAS',
    "maintainer": "",
    "website": 'https://www.plastiventas.com',
    "depends": [
        'base',
        'mail',
        'product',
        ],
    "data": [
        
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/plastic_material_views.xml',
        'views/plastic_product_views.xml',
        'views/production_order_views.xml',
        'views/quality_control_views.xml',
        'views/customer_order_views.xml',
    ],
    "assets": {},
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": True
}