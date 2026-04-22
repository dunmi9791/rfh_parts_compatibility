# -*- coding: utf-8 -*-
from odoo import models, fields


class RFHVehicleModelExtension(models.Model):
    """Extend rfh.vehicle.model to add engine variants."""
    _inherit = "rfh.vehicle.model"

    engine_ids = fields.One2many(
        "spare.vehicle.engine", "model_id",
        string="Engine Variants",
    )
    engine_count = fields.Integer(
        string="# Engines",
        compute="_compute_engine_count",
    )

    def _compute_engine_count(self):
        for rec in self:
            rec.engine_count = len(rec.engine_ids)
