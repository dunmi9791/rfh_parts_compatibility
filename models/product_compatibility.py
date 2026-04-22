# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductCompatibility(models.Model):
    """
    Bridge record: one product template ↔ one vehicle spec.
    A part can have many of these lines — one per compatible vehicle.
    """
    _name = 'spare.product.compatibility'
    _description = 'Part–Vehicle Compatibility'
    _order = 'product_tmpl_id, vehicle_make_id, vehicle_model_id'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
        ondelete='cascade',
        index=True,
    )
    vehicle_make_id = fields.Many2one(
        'spare.vehicle.make',
        string='Make',
        required=True,
        ondelete='restrict',
        index=True,
    )
    vehicle_model_id = fields.Many2one(
        'spare.vehicle.model',
        string='Model',
        domain="[('make_id', '=', vehicle_make_id)]",
        ondelete='restrict',
        index=True,
    )
    engine_id = fields.Many2one(
        'spare.vehicle.engine',
        string='Engine',
        domain="[('model_id', '=', vehicle_model_id)]",
        ondelete='restrict',
    )
    year_from = fields.Integer(
        string='Year From',
        help='First model year this part fits (0 = all)',
    )
    year_to = fields.Integer(
        string='Year To',
        help='Last model year this part fits (0 = current)',
    )
    oem_part_number = fields.Char(
        string='OEM Part #',
        help='Original Equipment Manufacturer part number for cross-referencing',
        index=True,
    )
    fitment_notes = fields.Text(
        string='Fitment Notes',
        help='e.g. "Fits 4WD only" or "Not for facelift models"',
    )

    # Computed summary displayed in the list
    summary = fields.Char(
        string='Compatibility',
        compute='_compute_summary', store=True,
    )

    @api.depends('vehicle_make_id.name', 'vehicle_model_id.name',
                 'engine_id.name', 'year_from', 'year_to')
    def _compute_summary(self):
        for rec in self:
            parts = []
            if rec.vehicle_make_id:
                parts.append(rec.vehicle_make_id.name)
            if rec.vehicle_model_id:
                parts.append(rec.vehicle_model_id.name)
            if rec.engine_id:
                parts.append(f'[{rec.engine_id.name}]')
            if rec.year_from or rec.year_to:
                y_from = str(rec.year_from) if rec.year_from else '?'
                y_to   = str(rec.year_to)   if rec.year_to   else 'present'
                parts.append(f'({y_from}–{y_to})')
            rec.summary = ' '.join(parts)

    @api.constrains('year_from', 'year_to')
    def _check_years(self):
        for rec in self:
            if rec.year_from and rec.year_to and rec.year_from > rec.year_to:
                raise ValidationError(
                    f'Year From ({rec.year_from}) cannot be after Year To ({rec.year_to}).'
                )

    @api.onchange('vehicle_make_id')
    def _onchange_make(self):
        """Clear model/engine when make changes."""
        self.vehicle_model_id = False
        self.engine_id = False

    @api.onchange('vehicle_model_id')
    def _onchange_model(self):
        """Clear engine when model changes."""
        self.engine_id = False
