# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class PartFinderWizard(models.TransientModel):
    """Find Parts for Vehicle wizard. Auto-fills from job card context."""
    _name = "spare.part.finder"
    _description = "Find Parts for Vehicle"

    vehicle_id = fields.Many2one("rfh.vehicle", string="Vehicle",
        help="Select a registered vehicle to auto-fill make/model/engine.")
    job_card_id = fields.Many2one("rfh.job.card", string="Job Card")

    vehicle_make_id  = fields.Many2one("rfh.vehicle.make",  string="Make",  required=True)
    vehicle_model_id = fields.Many2one("rfh.vehicle.model", string="Model",
        domain="[('make_id', '=', vehicle_make_id)]")
    engine_id = fields.Many2one("spare.vehicle.engine", string="Engine",
        domain="[('model_id', '=', vehicle_model_id)]")
    year = fields.Integer(string="Year", help="0 = all years")
    category_id = fields.Many2one("product.category", string="Part Category")

    @api.onchange("vehicle_id")
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.vehicle_make_id  = self.vehicle_id.make_id
            self.vehicle_model_id = self.vehicle_id.model_id
            self.engine_id        = self.vehicle_id.engine_id
            self.year = int(self.vehicle_id.year) if self.vehicle_id.year else 0

    @api.onchange("job_card_id")
    def _onchange_job_card(self):
        if self.job_card_id and self.job_card_id.vehicle_id:
            self.vehicle_id = self.job_card_id.vehicle_id
            self._onchange_vehicle()

    @api.onchange("vehicle_make_id")
    def _onchange_make(self):
        if not self.vehicle_id:
            self.vehicle_model_id = False
            self.engine_id = False

    @api.onchange("vehicle_model_id")
    def _onchange_model(self):
        if not self.vehicle_id:
            self.engine_id = False

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ctx = self.env.context
        if ctx.get("default_vehicle_make_id"):
            res["vehicle_make_id"] = ctx["default_vehicle_make_id"]
        if ctx.get("default_vehicle_model_id"):
            res["vehicle_model_id"] = ctx["default_vehicle_model_id"]
        if ctx.get("default_engine_id"):
            res["engine_id"] = ctx["default_engine_id"]
        if ctx.get("default_year"):
            res["year"] = ctx["default_year"]
        if ctx.get("default_job_card_id"):
            res["job_card_id"] = ctx["default_job_card_id"]
        return res

    def _get_compatible_product_ids(self):
        self.ensure_one()
        if not self.vehicle_make_id:
            return []
        domain = [("vehicle_make_id", "=", self.vehicle_make_id.id)]
        if self.vehicle_model_id:
            domain += ["|",
                ("vehicle_model_id", "=", False),
                ("vehicle_model_id", "=", self.vehicle_model_id.id)]
        if self.engine_id:
            domain += ["|",
                ("engine_id", "=", False),
                ("engine_id", "=", self.engine_id.id)]
        if self.year:
            domain += [
                "|", ("year_from", "=", 0), ("year_from", "<=", self.year),
                "|", ("year_to",   "=", 0), ("year_to",   ">=", self.year),
            ]
        compat = self.env["spare.product.compatibility"].search(domain)
        tmpl_ids = compat.mapped("product_tmpl_id").ids
        prod_domain = [("id", "in", tmpl_ids)]
        if self.category_id:
            cat_ids = self.env["product.category"].search(
                [("id", "child_of", self.category_id.id)]
            ).ids
            prod_domain += [("categ_id", "in", cat_ids)]
        return self.env["product.template"].search(prod_domain).ids

    def action_find_parts(self):
        self.ensure_one()
        tmpl_ids = self._get_compatible_product_ids()
        label = self.vehicle_make_id.name
        if self.vehicle_model_id:
            label += " %s" % self.vehicle_model_id.name
        if self.year:
            label += " (%s)" % self.year
        if not tmpl_ids:
            raise UserError(
                "No parts found for %s.\n\n"
                "Add compatibility entries on the product's "
                "Vehicle Compatibility tab first." % label
            )
        return {
            "type": "ir.actions.act_window",
            "name": "Compatible Parts - %s" % label,
            "res_model": "product.template",
            "view_mode": "list,kanban,form",
            "domain": [("id", "in", tmpl_ids)],
        }
