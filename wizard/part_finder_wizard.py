# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class PartFinderWizard(models.TransientModel):
    """
    "Find Parts for Vehicle" wizard.
    Select a make / model / engine / year and get back every product
    that has a matching compatibility entry.
    Can be launched standalone or from a repair/job-card record.
    """
    _name = 'spare.part.finder'
    _description = 'Find Parts for Vehicle'

    # ── Filters ───────────────────────────────────────────────────────────────
    vehicle_make_id = fields.Many2one(
        'spare.vehicle.make', string='Make', required=True,
    )
    vehicle_model_id = fields.Many2one(
        'spare.vehicle.model', string='Model',
        domain="[('make_id', '=', vehicle_make_id)]",
    )
    engine_id = fields.Many2one(
        'spare.vehicle.engine', string='Engine',
        domain="[('model_id', '=', vehicle_model_id)]",
    )
    year = fields.Integer(
        string='Year',
        help='Enter the vehicle year to narrow results (leave 0 for all years)',
    )
    category_id = fields.Many2one(
        'product.category', string='Part Category',
        help='Optionally filter by product category',
    )

    # ── Results (read-only) ───────────────────────────────────────────────────
    result_count = fields.Integer(
        string='Parts Found', compute='_compute_result_count',
    )

    @api.depends('vehicle_make_id', 'vehicle_model_id', 'engine_id', 'year', 'category_id')
    def _compute_result_count(self):
        for wiz in self:
            wiz.result_count = len(wiz._get_domain())

    # ── Onchange cascades ─────────────────────────────────────────────────────
    @api.onchange('vehicle_make_id')
    def _onchange_make(self):
        self.vehicle_model_id = False
        self.engine_id = False

    @api.onchange('vehicle_model_id')
    def _onchange_model(self):
        self.engine_id = False

    # ── Domain builder ────────────────────────────────────────────────────────
    def _get_domain(self):
        """Return list of product.template ids that match the current filters."""
        self.ensure_one()
        if not self.vehicle_make_id:
            return []

        compat_domain = [
            ('vehicle_make_id', '=', self.vehicle_make_id.id),
        ]
        if self.vehicle_model_id:
            compat_domain += [('vehicle_model_id', '=', self.vehicle_model_id.id)]
        if self.engine_id:
            compat_domain += [('engine_id', '=', self.engine_id.id)]
        if self.year:
            compat_domain += [
                '|', ('year_from', '=', 0), ('year_from', '<=', self.year),
                '|', ('year_to', '=', 0),   ('year_to', '>=', self.year),
            ]

        compat_records = self.env['spare.product.compatibility'].search(compat_domain)
        tmpl_ids = compat_records.mapped('product_tmpl_id').ids

        # Apply category filter on top
        prod_domain = [('id', 'in', tmpl_ids)]
        if self.category_id:
            # Include child categories
            cat_ids = self.env['product.category'].search(
                [('id', 'child_of', self.category_id.id)]
            ).ids
            prod_domain += [('categ_id', 'in', cat_ids)]

        return self.env['product.template'].search(prod_domain).ids

    # ── Actions ───────────────────────────────────────────────────────────────
    def action_find_parts(self):
        """Open product list filtered to compatible parts."""
        self.ensure_one()
        tmpl_ids = self._get_domain()
        if not tmpl_ids:
            raise UserError(
                f'No parts found for {self.vehicle_make_id.name}'
                + (f' {self.vehicle_model_id.name}' if self.vehicle_model_id else '')
                + (f' ({self.year})' if self.year else '')
                + '. Check the Vehicle Compatibility tab on your products.'
            )
        return {
            'type': 'ir.actions.act_window',
            'name': 'Compatible Parts',
            'res_model': 'product.template',
            'view_mode': 'list,kanban,form',
            'domain': [('id', 'in', tmpl_ids)],
            'context': {
                'search_default_filter_to_sell': 0,
                'search_default_filter_to_purchase': 0,
            },
        }
