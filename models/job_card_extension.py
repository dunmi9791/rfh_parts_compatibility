# -*- coding: utf-8 -*-
from odoo import models


class JobCardPartFinderExtension(models.Model):
    """
    Add 'Find Parts for Vehicle' action to rfh.job.card.
    Launches the part-finder wizard pre-filled with the job's vehicle details.
    """
    _inherit = 'rfh.job.card'

    def action_open_part_finder(self):
        self.ensure_one()
        vehicle = self.vehicle_id
        if not vehicle:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'Please select a vehicle for this job card first.',
                    'type': 'warning',
                },
            }

        return {
            'type': 'ir.actions.act_window',
            'name': f'Find Parts — {vehicle.name}',
            'res_model': 'spare.part.finder',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_make_id':  vehicle.make_id.id  if vehicle.make_id  else False,
                'default_vehicle_model_id': vehicle.model_id.id if vehicle.model_id else False,
                'default_engine_id':        vehicle.engine_id.id if vehicle.engine_id else False,
                'default_year':             int(vehicle.year) if vehicle.year else 0,
                'default_job_card_id':      self.id,
            },
        }
