# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleEngine(models.Model):
    """Engine / drivetrain variant for a vehicle model."""
    _name = 'spare.vehicle.engine'
    _description = 'Vehicle Engine Variant'
    _order = 'model_id, name asc'
    _rec_name = 'full_name'

    name = fields.Char(
        string='Engine Code / Name', required=True,
        help='e.g. "2.8L 1GD-FTV Diesel" or "1.5L VTEC Petrol"',
    )
    model_id = fields.Many2one(
        'spare.vehicle.model', string='Vehicle Model',
        required=True, ondelete='cascade', index=True,
    )
    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name', store=True,
    )
    fuel_type = fields.Selection([
        ('diesel',   'Diesel'),
        ('petrol',   'Petrol'),
        ('hybrid',   'Hybrid'),
        ('electric', 'Electric'),
        ('lpg',      'LPG'),
    ], string='Fuel Type')
    displacement = fields.Float(string='Displacement (L)', digits=(3, 1))
    cylinders = fields.Integer(string='Cylinders')
    power_hp = fields.Integer(string='Power (hp)')
    active = fields.Boolean(default=True)
    notes = fields.Text()

    @api.depends('model_id.full_name', 'name')
    def _compute_full_name(self):
        for rec in self:
            model = rec.model_id.full_name or ''
            rec.full_name = f'{model} — {rec.name}'.strip(' —')

    def name_get(self):
        return [(rec.id, rec.full_name) for rec in self]
