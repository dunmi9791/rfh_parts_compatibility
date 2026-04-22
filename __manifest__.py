# -*- coding: utf-8 -*-
{
    'name': 'RFH Vehicle Parts Compatibility',
    'version': '18.0.1.0.0',
    'summary': 'Link workshop parts to vehicle makes, models and engines',
    'description': """
RFH Vehicle Parts Compatibility
================================
Adds a Vehicle Compatibility layer on top of the RFH Workshop Management module.

Features:
- Vehicle Make / Model / Engine catalogue (Toyota, Honda, Nissan, …)
- Compatibility tab on every product: map a part to the vehicles it fits
- "Find Parts for Vehicle" wizard — search compatible parts from any repair job
- Seed data for the most common makes/models serviced at Riders Workshop
    """,
    'category': 'Manufacturing/Maintenance',
    'author': 'Riders Workshop',
    'website': 'https://ridersng.org',
    'license': 'LGPL-3',

    'depends': [
        'product',
        'stock',
        'rfh_workshop_management',
    ],

    'data': [
        # Security first
        'security/rfh_parts_security.xml',
        'security/ir.model.access.csv',

        # Core views
        'views/vehicle_make_views.xml',
        'views/vehicle_model_views.xml',
        'views/vehicle_engine_views.xml',
        'views/product_compatibility_views.xml',

        # Wizard
        'wizard/part_finder_wizard_views.xml',

        # Menus
        'views/menus.xml',

        # Seed data — load after views so noupdate works
        'data/vehicle_data.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
