# -*- coding: utf-8 -*-
{
    'name': 'RFH Vehicle Parts Compatibility',
    'version': '18.0.2.0.0',
    'summary': 'Link workshop parts to vehicles; find compatible parts from any job card',
    'description': """
RFH Vehicle Parts Compatibility
================================
Integrates with rfh_workshop_management to add:

- Engine variants on the existing Vehicle Make/Model catalogue
- Engine field on registered vehicles (rfh.vehicle)
- "Vehicle Compatibility" tab on every product
- One-click "Find Parts for Vehicle" button on job cards
- Compatibility indicator (✅ / ⚠️) on every parts line in a job card
- Part finder wizard — auto-filled from the job's vehicle
    """,
    'category': 'Manufacturing/Maintenance',
    'author': 'Riders Workshop',
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

        # Extend existing vehicle views (make, model) before engine view
        'views/vehicle_make_views.xml',
        'views/vehicle_model_views.xml',

        # New: engine variant view
        'views/vehicle_engine_views.xml',

        # Product compatibility tab
        'views/product_compatibility_views.xml',

        # Job card + vehicle form extensions
        'views/job_card_extension_views.xml',

        # Part finder wizard
        'wizard/part_finder_wizard_views.xml',

        # Menus
        'views/menus.xml',

        # Seed data placeholder (actual seeding in post_init_hook)
        'data/vehicle_data.xml',
    ],

    'post_init_hook': 'post_init_hook',

    'installable': True,
    'application': False,
    'auto_install': False,
}
