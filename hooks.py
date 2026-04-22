# -*- coding: utf-8 -*-
"""
post_init_hook: safely seeds vehicle makes, models, and engines
using get-or-create so it never duplicates existing records.
"""

VEHICLE_DATA = [
    # (make_name, [(model_name, [(engine_name, fuel, displacement, cylinders, hp)])])
    ('Toyota', [
        ('Hilux', [
            ('2.4L 2GD-FTV Diesel',    'diesel', 2.4, 4, 150),
            ('2.8L 1GD-FTV Diesel',    'diesel', 2.8, 4, 177),
            ('2.7L 2TR-FE Petrol',     'petrol', 2.7, 4, 160),
            ('3.0L 1KD-FTV Diesel',    'diesel', 3.0, 4, 163),
        ]),
        ('Land Cruiser Prado', [
            ('2.8L 1GD-FTV Diesel',    'diesel', 2.8, 4, 177),
            ('3.0L 1KD-FTV Diesel',    'diesel', 3.0, 4, 163),
            ('4.0L 1GR-FE V6 Petrol',  'petrol', 4.0, 6, 282),
        ]),
        ('Land Cruiser 200', [
            ('4.5L 1VD-FTV V8 Diesel', 'diesel', 4.5, 8, 232),
            ('4.7L 2UZ-FE V8 Petrol',  'petrol', 4.7, 8, 288),
        ]),
        ('Fortuner', [
            ('2.4L 2GD-FTV Diesel',    'diesel', 2.4, 4, 150),
            ('2.8L 1GD-FTV Diesel',    'diesel', 2.8, 4, 177),
            ('4.0L 1GR-FE V6 Petrol',  'petrol', 4.0, 6, 282),
        ]),
        ('Camry', [
            ('2.5L 2AR-FE Petrol',     'petrol', 2.5, 4, 181),
            ('2.4L 2AZ-FE Petrol',     'petrol', 2.4, 4, 167),
        ]),
        ('Corolla', [
            ('1.8L 2ZR-FE Petrol',     'petrol', 1.8, 4, 140),
            ('1.6L 1ZR-FE Petrol',     'petrol', 1.6, 4, 122),
        ]),
        ('Hiace', [
            ('2.5L 2KD-FTV Diesel',    'diesel', 2.5, 4, 102),
            ('2.0L 1TR-FE Petrol',     'petrol', 2.0, 4, 136),
        ]),
        ('Avensis', [
            ('2.0L 1AD-FTV Diesel',    'diesel', 2.0, 4, 126),
            ('2.2L 2AD-FHV Diesel',    'diesel', 2.2, 4, 150),
        ]),
        ('RAV4', [
            ('2.5L 2AR-FE Petrol',     'petrol', 2.5, 4, 181),
            ('2.0L 3ZR-FE Petrol',     'petrol', 2.0, 4, 151),
        ]),
        ('Yaris', [
            ('1.5L 1NZ-FE Petrol',     'petrol', 1.5, 4, 106),
            ('1.3L 2NZ-FE Petrol',     'petrol', 1.3, 4, 87),
        ]),
    ]),
    ('Honda', [
        ('Civic', [
            ('1.8L R18A Petrol',           'petrol', 1.8, 4, 140),
            ('1.5L L15B7 VTEC Turbo',      'petrol', 1.5, 4, 174),
            ('2.0L K20C Type R Turbo',     'petrol', 2.0, 4, 316),
        ]),
        ('Accord', [
            ('2.4L K24A Petrol',           'petrol', 2.4, 4, 190),
            ('3.0L J30A V6 Petrol',        'petrol', 3.0, 6, 244),
            ('1.5L VTEC Turbo Petrol',     'petrol', 1.5, 4, 192),
        ]),
        ('CR-V', [
            ('2.4L K24Z Petrol',           'petrol', 2.4, 4, 185),
            ('1.5L VTEC Turbo Petrol',     'petrol', 1.5, 4, 190),
            ('2.0L i-MMD Hybrid',          'hybrid', 2.0, 4, 212),
        ]),
        ('HR-V', [
            ('1.8L R18Z Petrol',           'petrol', 1.8, 4, 141),
            ('1.5L L15B VTEC Petrol',      'petrol', 1.5, 4, 131),
        ]),
        ('Pilot', [
            ('3.5L J35Y V6 Petrol',        'petrol', 3.5, 6, 280),
        ]),
        ('Odyssey', [
            ('3.5L J35Y V6 Petrol',        'petrol', 3.5, 6, 280),
        ]),
    ]),
    ('Nissan', [
        ('Patrol', [
            ('5.6L VK56VD V8 Petrol',  'petrol', 5.6, 8, 400),
            ('3.0L ZD30DDTi Diesel',   'diesel', 3.0, 4, 158),
            ('4.8L TB48DE Petrol',     'petrol', 4.8, 6, 272),
        ]),
        ('Navara', [
            ('2.5L YD25DDTi Diesel',   'diesel', 2.5, 4, 174),
            ('2.5L QR25DE Petrol',     'petrol', 2.5, 4, 171),
        ]),
        ('Pathfinder', [
            ('3.5L VQ35DE V6 Petrol',  'petrol', 3.5, 6, 284),
            ('2.5L YD25DDTi Diesel',   'diesel', 2.5, 4, 190),
        ]),
        ('Altima', [
            ('2.5L QR25DE Petrol',     'petrol', 2.5, 4, 182),
            ('3.5L VQ35DE V6 Petrol',  'petrol', 3.5, 6, 270),
        ]),
        ('Sentra', [
            ('1.8L MRA8DE Petrol',     'petrol', 1.8, 4, 130),
        ]),
        ('X-Terra', [
            ('2.5L YD25DDTi Diesel',   'diesel', 2.5, 4, 174),
        ]),
    ]),
    ('Ford', [
        ('Ranger', [
            ('2.2L TDCi Diesel',       'diesel', 2.2, 4, 160),
            ('3.2L TDCi Diesel',       'diesel', 3.2, 5, 197),
            ('2.0L EcoBlue Diesel',    'diesel', 2.0, 4, 213),
        ]),
        ('Explorer', [
            ('3.5L EcoBoost V6 Petrol', 'petrol', 3.5, 6, 365),
            ('2.3L EcoBoost Petrol',    'petrol', 2.3, 4, 300),
        ]),
        ('Escape / Kuga', [
            ('1.5L EcoBoost Petrol',   'petrol', 1.5, 4, 182),
            ('2.0L EcoBlue Diesel',    'diesel', 2.0, 4, 150),
        ]),
    ]),
    ('Hyundai', [
        ('Elantra', [
            ('2.0L Nu MPI Petrol',     'petrol', 2.0, 4, 152),
            ('1.6L GDI Petrol',        'petrol', 1.6, 4, 130),
        ]),
        ('Tucson', [
            ('2.0L Nu MPI Petrol',     'petrol', 2.0, 4, 155),
            ('1.6L CRDi Diesel',       'diesel', 1.6, 4, 136),
        ]),
        ('Santa Fe', [
            ('2.2L CRDi Diesel',       'diesel', 2.2, 4, 197),
            ('2.4L GDI Petrol',        'petrol', 2.4, 4, 188),
        ]),
        ('iX35', [
            ('2.0L MPI Petrol',        'petrol', 2.0, 4, 155),
            ('1.7L CRDi Diesel',       'diesel', 1.7, 4, 114),
        ]),
    ]),
    ('Lexus', [
        ('LX 570', [
            ('5.7L 3UR-FE V8 Petrol',  'petrol', 5.7, 8, 383),
        ]),
        ('GX 460', [
            ('4.6L 1UR-FE V8 Petrol',  'petrol', 4.6, 8, 301),
        ]),
        ('RX 350', [
            ('3.5L 2GR-FKS V6 Petrol', 'petrol', 3.5, 6, 295),
        ]),
    ]),
    ('Mercedes-Benz', [
        ('C-Class', [
            ('2.0L M254 Petrol',       'petrol', 2.0, 4, 204),
            ('2.0L OM654 Diesel',      'diesel', 2.0, 4, 200),
        ]),
        ('E-Class', [
            ('2.0L M254 Petrol',       'petrol', 2.0, 4, 258),
            ('2.0L OM654 Diesel',      'diesel', 2.0, 4, 194),
        ]),
        ('G-Class', [
            ('4.0L M176 V8 Biturbo',   'petrol', 4.0, 8, 585),
        ]),
    ]),
    ('Kia', [
        ('Sportage', [
            ('2.0L MPI Petrol',        'petrol', 2.0, 4, 155),
            ('1.6L CRDi Diesel',       'diesel', 1.6, 4, 136),
        ]),
        ('Sorento', [
            ('2.2L CRDi Diesel',       'diesel', 2.2, 4, 197),
            ('3.5L Lambda V6 Petrol',  'petrol', 3.5, 6, 278),
        ]),
    ]),
]


def post_init_hook(env):
    """
    Seed vehicle makes, models, and engine variants.
    Uses get-or-create so it is safe to run multiple times.
    """
    Make  = env['rfh.vehicle.make']
    Model = env['rfh.vehicle.model']
    Eng   = env['spare.vehicle.engine']

    for make_name, models in VEHICLE_DATA:
        make = Make.search([('name', '=', make_name)], limit=1)
        if not make:
            make = Make.create({'name': make_name})

        for model_name, engines in models:
            model = Model.search(
                [('name', '=', model_name), ('make_id', '=', make.id)], limit=1
            )
            if not model:
                model = Model.create({'name': model_name, 'make_id': make.id})

            for eng_name, fuel, disp, cyl, hp in engines:
                existing = Eng.search(
                    [('name', '=', eng_name), ('model_id', '=', model.id)], limit=1
                )
                if not existing:
                    Eng.create({
                        'name':         eng_name,
                        'model_id':     model.id,
                        'fuel_type':    fuel,
                        'displacement': disp,
                        'cylinders':    cyl,
                        'power_hp':     hp,
                    })
