# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RFHVehicleMakeExtension(models.Model):
    """Extend rfh.vehicle.make with a compatible-parts count."""
    _inherit = "rfh.vehicle.make"

    compatibility_count = fields.Integer(
        string="Compatible Parts",
        compute="_compute_compatibility_count",
    )

    logo = fields.Binary(
        string="Logo",
        attachment=True,
    )

    notes = fields.Text(
        string="Notes",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    model_count = fields.Integer(
        string="# Models",
        compute="_compute_model_count",
    )

    @api.depends("model_ids")
    def _compute_model_count(self):
        for rec in self:
            rec.model_count = len(rec.model_ids)

    @api.depends("model_ids")
    def _compute_compatibility_count(self):
        for make in self:
            make.compatibility_count = self.env["spare.product.compatibility"].search_count(
                [("vehicle_make_id", "=", make.id)]
            )

    def action_view_models(self):
        """Action for the 'Models' stat button."""
        self.ensure_one()
        return {
            "name": "Models",
            "type": "ir.actions.act_window",
            "res_model": "rfh.vehicle.model",
            "view_mode": "list,form",
            "domain": [("make_id", "=", self.id)],
            "context": {"default_make_id": self.id},
        }

    def action_view_parts(self):
        """Action for the 'Compatible Parts' stat button."""
        self.ensure_one()
        return {
            "name": "Compatible Parts",
            "type": "ir.actions.act_window",
            "res_model": "spare.product.compatibility",
            "view_mode": "list,form",
            "domain": [("vehicle_make_id", "=", self.id)],
            "context": {"default_vehicle_make_id": self.id},
        }
