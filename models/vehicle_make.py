# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VehicleMake(models.Model):
    """Vehicle manufacturer — Toyota, Honda, Nissan, etc."""
    _name = 'spare.vehicle.make'
    _description = 'Vehicle Make'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string='Make', required=True, index=True)
    logo = fields.Image(string='Logo', max_width=128, max_height=128)
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes')

    model_ids = fields.One2many(
        'spare.vehicle.model', 'make_id',
        string='Models',
    )
    model_count = fields.Integer(
        string='# Models',
        compute='_compute_model_count',
    )

    @api.depends('model_ids')
    def _compute_model_count(self):
        for rec in self:
            rec.model_count = len(rec.model_ids)

    def action_view_models(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.name} Models',
            'res_model': 'spare.vehicle.model',
            'view_mode': 'list,form',
            'domain': [('make_id', '=', self.id)],
            'context': {'default_make_id': self.id},
        }
