from odoo import models, fields, api


class MaintenanceRequestDoneWizard(models.TransientModel):
    _name = 'maintenance.request.done.wizard'
    _description = 'Maintenance Request Done Wizard'

    choice = fields.Selection([
        ('fixed', 'Fixed'),
        ('replaced', 'Replaced')
    ], string='Action', required=True)
    description = fields.Text(string='Description')

    def apply_choice(self):
        maintenance_request = self.env['maintenance.request'].browse(self.env.context.get('active_id'))
        maintenance_request.done_choice = self.choice
        maintenance_request.done_description = self.description
        maintenance_request.stop_timer()  # Stop the timer
        maintenance_request.complete_request()  # Call the complete_request method to change stage
        return {'type': 'ir.actions.act_window_close'}
