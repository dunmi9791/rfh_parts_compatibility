# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleModel(models.Model):
    """Vehicle model — Hilux, Civic, Patrol, etc."""
    _name = 'spare.vehicle.model'
    _description = 'Vehicle Model'
    _order = 'make_id, name asc'
    _rec_name = 'full_name'

    name = fields.Char(string='Model Name', required=True, index=True)
    make_id = fields.Many2one(
        'spare.vehicle.make', string='Make',
        required=True, ondelete='cascade', index=True,
    )
    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name', store=True, index=True,
    )
    body_type = fields.Selection([
        ('sedan',   'Sedan'),
        ('suv',     'SUV / Crossover'),
        ('pickup',  'Pickup / Truck'),
        ('van',     'Van / Minibus'),
        ('bus',     'Bus'),
        ('coupe',   'Coupe'),
        ('wagon',   'Estate / Wagon'),
        ('other',   'Other'),
    ], string='Body Type')
    year_from = fields.Integer(string='Year From')
    year_to = fields.Integer(string='Year To', help='Leave 0 for current production')
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes')

    engine_ids = fields.One2many(
        'spare.vehicle.engine', 'model_id',
        string='Engine Variants',
    )
    engine_count = fields.Integer(
        string='# Engines',
        compute='_compute_engine_count',
    )

    @api.depends('make_id.name', 'name')
    def _compute_full_name(self):
        for rec in self:
            make = rec.make_id.name or ''
            rec.full_name = f'{make} {rec.name}'.strip()

    @api.depends('engine_ids')
    def _compute_engine_count(self):
        for rec in self:
            rec.engine_count = len(rec.engine_ids)

    def name_get(self):
        result = []
        for rec in self:
            year_str = ''
            if rec.year_from:
                to = str(rec.year_to) if rec.year_to else 'present'
                year_str = f' ({rec.year_from}–{to})'
            result.append((rec.id, f'{rec.full_name}{year_str}'))
        return result
