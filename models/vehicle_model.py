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
    compatibility_count = fields.Integer(
        string="Compatible Parts",
        compute="_compute_compatibility_count",
    )

    body_type = fields.Selection([
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('van', 'Van'),
        ('other', 'Other'),
    ], string="Body Type")

    year_from = fields.Integer(string="Year From")
    year_to = fields.Integer(string="Year To")

    notes = fields.Text(
        string="Notes",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    def _compute_engine_count(self):
        for rec in self:
            rec.engine_count = len(rec.engine_ids)

    def _compute_compatibility_count(self):
        for rec in self:
            rec.compatibility_count = self.env["spare.product.compatibility"].search_count(
                [("vehicle_model_id", "=", rec.id)]
            )

    def action_view_engines(self):
        """Action for the 'Engines' stat button."""
        self.ensure_one()
        return {
            "name": "Engines",
            "type": "ir.actions.act_window",
            "res_model": "spare.vehicle.engine",
            "view_mode": "list,form",
            "domain": [("model_id", "=", self.id)],
            "context": {"default_model_id": self.id},
        }

    def action_view_parts(self):
        """Action for the 'Compatible Parts' stat button."""
        self.ensure_one()
        return {
            "name": "Compatible Parts",
            "type": "ir.actions.act_window",
            "res_model": "spare.product.compatibility",
            "view_mode": "list,form",
            "domain": [("vehicle_model_id", "=", self.id)],
            "context": {"default_vehicle_model_id": self.id},
        }
