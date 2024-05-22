from odoo import models, fields, api


class AssignTechnicianWizard(models.TransientModel):
    _name = 'assign.technician.wizard'
    _description = 'Assign Technician Wizard'

    maintenance_team_id = fields.Many2one('maintenance.team', string='Team', readonly=True)
    user_id = fields.Many2one('res.users', string='Technician', domain="[('id', 'in', team_member_ids)]")
    team_member_ids = fields.Many2many('res.users', compute='_compute_team_members', store=False)

    @api.depends('maintenance_team_id')
    def _compute_team_members(self):
        for wizard in self:
            wizard.team_member_ids = wizard.maintenance_team_id.member_ids.ids

    def assign_technician(self):
        maintenance_request = self.env['maintenance.request'].browse(self.env.context.get('active_id'))
        maintenance_request.user_id = self.user_id.id
        #assigned_stage = self.env['maintenance.stage'].search([('name', '=', 'Assigned')], limit=1)
        maintenance_request.state = 'assigned'
        return {'type': 'ir.actions.act_window_close'}
