# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RFHVehicleMakeExtension(models.Model):
    """Extend rfh.vehicle.make with a compatible-parts count."""
    _inherit = "rfh.vehicle.make"

    compatibility_count = fields.Integer(
        string="Compatible Parts",
        compute="_compute_compatibility_count",
    )

    @api.depends("model_ids")
    def _compute_compatibility_count(self):
        for make in self:
            make.compatibility_count = self.env["spare.product.compatibility"].search_count(
                [("vehicle_make_id", "=", make.id)]
            )
