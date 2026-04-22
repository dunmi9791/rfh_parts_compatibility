# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleEngine(models.Model):
    """Engine/drivetrain variant linked to the existing rfh.vehicle.model."""
    _name = "spare.vehicle.engine"
    _description = "Vehicle Engine Variant"
    _order = "model_id, name asc"
    _rec_name = "full_name"

    name = fields.Char(
        string="Engine Code / Name", required=True,
        help="e.g. 2.8L 1GD-FTV Diesel",
    )
    model_id = fields.Many2one(
        "rfh.vehicle.model",
        string="Vehicle Model",
        required=True, ondelete="cascade", index=True,
    )
    make_id = fields.Many2one(
        "rfh.vehicle.make",
        string="Make",
        related="model_id.make_id", store=True, readonly=True,
    )
    full_name = fields.Char(
        string="Full Name",
        compute="_compute_full_name", store=True,
    )
    fuel_type = fields.Selection([
        ("diesel",   "Diesel"),
        ("petrol",   "Petrol"),
        ("hybrid",   "Hybrid"),
        ("electric", "Electric"),
        ("lpg",      "LPG"),
    ], string="Fuel Type")
    displacement = fields.Float(string="Displacement (L)", digits=(3, 1))
    cylinders = fields.Integer(string="Cylinders")
    power_hp = fields.Integer(string="Power (hp)")
    active = fields.Boolean(default=True)
    notes = fields.Text()

    @api.depends("model_id.name", "model_id.make_id.name", "name")
    def _compute_full_name(self):
        for rec in self:
            make  = rec.model_id.make_id.name or ""
            model = rec.model_id.name or ""
            rec.full_name = "%s %s - %s" % (make, model, rec.name)

    def name_get(self):
        return [(rec.id, rec.full_name) for rec in self]
