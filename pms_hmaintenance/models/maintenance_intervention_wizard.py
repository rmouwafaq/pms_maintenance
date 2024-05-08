from odoo import models, fields, api


class MaintenanceInterventionWizard(models.TransientModel):
    _name = 'maintenance.intervention.wizard'
    _description = 'Maintenance Intervention Wizard'

    claimant_id = fields.Many2one('res.users', string='Claimant', required=True)
    equipment_category_id = fields.Many2one(
        'maintenance.equipment.category', string='Equipment Category', required=True)
    equipment_id = fields.Many2one(
        'maintenance.equipment', string='Equipment', required=True,
        domain="[('category_id', '=', equipment_category_id)]")
    intervention_type_id = fields.Many2one(
        'intervention_type', string='Intervention Type', required=True,
        domain="[('equipment_category_id', '=', equipment_category_id)]")
    hk_area_id = fields.Many2one('hk_area', string='HK Area', required=True)
    claim_time = fields.Datetime(string='Claim Time', required=True)
    photo_ids = fields.Many2many(
        'ir.attachment',
        'maintenance_intervention_wizard_ir_attachments_rel',
        'wizard_id', 'attachment_id',
        string="Photos")
    maintenance_team_id = fields.Many2one(
        'maintenance.team', string='Maintenance Team', required=False,
        domain="[('id', '=', equipment_id.maintenance_team_id)]")
    icon_image = fields.Binary(string="Intervention Icon", compute="_compute_icon_image", readonly=True)

    @api.depends('intervention_type_id')
    def _compute_icon_image(self):
        for record in self:
            record.icon_image = record.intervention_type_id.image if record.intervention_type_id else False

    @api.onchange('equipment_category_id')
    def _onchange_equipment_category_id(self):
        self.intervention_type_id = False
        self.equipment_id = False
        return {
            'domain': {
                'intervention_type_id': [('equipment_category_id', '=', self.equipment_category_id.id)],
                'equipment_id': [('category_id', '=', self.equipment_category_id.id)]
            }
        }

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id and self.equipment_id.maintenance_team_id:
            self.maintenance_team_id = self.equipment_id.maintenance_team_id
            return {'domain': {'maintenance_team_id': [('id', '=', self.equipment_id.maintenance_team_id.id)]}}
        else:
            self.maintenance_team_id = False
            return {'domain': {'maintenance_team_id': [('id', 'in', [])]}}

    def create_maintenance_request(self):
        self.ensure_one()
        maintenance_request_obj = self.env['maintenance.request']
        vals = {
            'name': f"{self.claimant_id.name} - {self.intervention_type_id.name}",
            'equipment_id': self.equipment_id.id,
            'category_id': self.equipment_category_id.id,
            'request_date': self.claim_time,
            'maintenance_type': 'corrective',
            'hk_area_id': self.hk_area_id.id,
            'intervention_type_id': self.intervention_type_id.id,
            'claimant_id': self.claimant_id.id,
            'schedule_date': self.claim_time,
            'maintenance_team_id': self.maintenance_team_id.id,
            'icon_image': self.icon_image,
            'photo_ids': [(6, 0, self.photo_ids.ids)],
        }
        maintenance_request = maintenance_request_obj.create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Request',
            'res_model': 'maintenance.request',
            'view_mode': 'form',
            'res_id': maintenance_request.id,
            'target': 'current'
        }
