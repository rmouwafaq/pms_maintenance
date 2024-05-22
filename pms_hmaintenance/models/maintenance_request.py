from odoo import models, fields, api
from datetime import datetime


class MaintenanceRequestExtension(models.Model):
    _inherit = 'maintenance.request'

    hk_area_id = fields.Many2one('hk_area', string='HK Area')
    intervention_type_id = fields.Many2one('intervention_type', string='Intervention Type')
    claimant_id = fields.Many2one('res.users', string='Reported by')
    photo_ids = fields.Many2many(
        'ir.attachment',
        'maintenance_request_ir_attachment_rel',
        'maintenance_request_id', 'attachment_id',
        string="Photos"
    )
    icon_image = fields.Binary(string="Icon")
    timer_start_time = fields.Datetime(string="Timer Start Time")
    timer_stop_time = fields.Datetime(string="Timer Stop Time")
    elapsed_time = fields.Char(string="Elapsed Time", compute='_compute_elapsed_time')
    done_choice = fields.Selection([
        ('fixed', 'Fixed'),
        ('replaced', 'Replaced')
    ], string='Action')
    done_description = fields.Text(string='Description')
    state = fields.Selection([
        ('new', 'New'), ('assigned', 'Assigned'), ('inprogress', 'In Progress'),
        ('blocked', 'Blocked'), ('done', 'Done')
    ], string='State', default='new')

    def open_assign_wizard(self):
        return {
            'name': 'Assign Technician',
            'type': 'ir.actions.act_window',
            'res_model': 'assign.technician.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('pms_hmaintenance.view_assign_technician_wizard_form').id,
            'target': 'new',
            'context': {
                'default_maintenance_team_id': self.maintenance_team_id.id,
            },
        }

    def block_request(self):
        self.state = 'blocked'
        self.stop_timer()

    def start_request(self):
        self.state = 'inprogress'
        self.start_timer()

    def start_timer(self):
        self.timer_start_time = fields.Datetime.now()
        self.timer_stop_time = None

    def stop_timer(self):
        self.timer_stop_time = fields.Datetime.now()

    @api.depends('timer_start_time', 'timer_stop_time')
    def _compute_elapsed_time(self):
        for request in self:
            if request.timer_start_time:
                if request.timer_stop_time:
                    elapsed = fields.Datetime.from_string(request.timer_stop_time) - fields.Datetime.from_string(
                        request.timer_start_time)
                else:
                    elapsed = datetime.now() - fields.Datetime.from_string(request.timer_start_time)
                total_seconds = int(elapsed.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                request.elapsed_time = f"{hours}h {minutes}m {seconds}s"
            else:
                request.elapsed_time = '00h 00m 00s'

    def complete_request(self):
        self.state = 'done'
        self.stop_timer()

    def open_done_wizard(self):
        return {
            'name': 'Complete Maintenance Request',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request.done.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_choice': self.done_choice, 'default_description': self.done_description}
        }
