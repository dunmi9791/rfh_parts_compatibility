# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RFHVehicleEngineExtension(models.Model):
    """Add engine_id to rfh.vehicle so we know exactly which engine is fitted."""
    _inherit = 'rfh.vehicle'

    engine_id = fields.Many2one(
        'spare.vehicle.engine',
        string='Engine',
        domain="[('model_id', '=', model_id)]",
        help='Select the specific engine variant fitted to this vehicle.',
    )

    @api.onchange('model_id')
    def _onchange_model_clear_engine(self):
        """Clear engine when model changes to avoid stale engine selection."""
        self.engine_id = False

    def action_find_compatible_parts(self):
        """
        Launch the part-finder wizard pre-filled with this vehicle's
        make / model / engine / year. Call this from the job card.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Compatible Parts — {self.name}',
            'res_model': 'spare.part.finder',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_make_id': self.make_id.id,
                'default_vehicle_model_id': self.model_id.id,
                'default_engine_id': self.engine_id.id if self.engine_id else False,
                'default_year': int(self.year) if self.year else 0,
            },
        }


class JobCardPartExtension(models.Model):
    """
    Extend rfh.job.card.part to show vehicle-compatibility status
    so a technician knows at a glance if the part is verified for
    the job's vehicle.
    """
    _inherit = 'rfh.job.card.part'

    is_compatible = fields.Boolean(
        string='Verified for Vehicle',
        compute='_compute_is_compatible',
        help='Green if this part has a compatibility entry for the job vehicle.',
    )
    compatibility_warning = fields.Char(
        string='Compatibility',
        compute='_compute_is_compatible',
    )

    @api.depends('product_id', 'job_card_id.vehicle_id',
                 'job_card_id.vehicle_id.make_id',
                 'job_card_id.vehicle_id.model_id')
    def _compute_is_compatible(self):
        for line in self:
            vehicle = line.job_card_id.vehicle_id
            if not vehicle or not line.product_id:
                line.is_compatible = False
                line.compatibility_warning = ''
                continue

            # Check if a compatibility entry exists for this product + vehicle make
            compat = self.env['spare.product.compatibility'].search([
                ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                ('vehicle_make_id', '=', vehicle.make_id.id),
            ], limit=1)

            if compat:
                # Narrow check: does it also match the model?
                model_compat = compat.filtered(
                    lambda c: not c.vehicle_model_id or c.vehicle_model_id == vehicle.model_id
                ) if vehicle.model_id else compat

                line.is_compatible = bool(model_compat or compat)
                line.compatibility_warning = '✅ Verified' if (model_compat or compat) else '⚠️ Make only'
            else:
                line.is_compatible = False
                line.compatibility_warning = '⚠️ Not verified'
