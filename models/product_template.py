# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Extend product.template with a Vehicle Compatibility tab."""
    _inherit = 'product.template'

    compatibility_ids = fields.One2many(
        'spare.product.compatibility',
        'product_tmpl_id',
        string='Vehicle Compatibility',
    )
    compatible_vehicle_count = fields.Integer(
        string='Compatible Vehicles',
        compute='_compute_compatible_vehicle_count',
    )
    is_workshop_part = fields.Boolean(
        string='Workshop Part',
        default=False,
        help='Tick if this product is used as a spare part in workshop repairs.',
    )

    @api.depends('compatibility_ids')
    def _compute_compatible_vehicle_count(self):
        for tmpl in self:
            tmpl.compatible_vehicle_count = len(tmpl.compatibility_ids)

    def action_view_compatibility(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicle Compatibility',
            'res_model': 'spare.product.compatibility',
            'view_mode': 'list,form',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {'default_product_tmpl_id': self.id},
        }
