from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MaintenanceRequestExtension(models.Model):
    _inherit = 'maintenance.request'

    hk_area_id = fields.Many2one('hk_area', string='HK Area')
    intervention_type_id = fields.Many2one('intervention_type', string='Intervention Type')
    claimant_id = fields.Many2one('res.users', string='Claimant')
    photo_ids = fields.Many2many(
        'ir.attachment',
        'maintenance_request_ir_attachment_rel',
        'maintenance_request_id', 'attachment_id',
        string="Photos"
    )
    icon_image = fields.Binary(string="Icon")

    def send_to_technician(self):

        if not self.user_id:

            default_technician = self.env['res.users'].search([('is_technician', '=', True)], limit=1)
            if default_technician:
                self.user_id = default_technician
            else:
                raise UserError(_("No Responsible Technician assigned and no default technician found."))

        # Ensure the technician is correctly notified
        message = f"Please review the maintenance request: {self.name}"
        self.message_post(body=message, subject="Maintenance Request Assignment", subtype_xmlid="mail.mt_note",
                          partner_ids=[self.user_id.partner_id.id])

        return {
            'name': _('My Maintenance Requests'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'maintenance.request',
            'domain': [('user_id', '=', self.user_id.id)],
            'context': {'default_user_id': self.user_id.id}
        }
