from odoo import models, fields, api


class HkArea(models.Model):
    _name = 'hk_area'
    _description = 'Housekeeping Area'

    name = fields.Char(string='Area Name', required=True)
    description = fields.Text(string='Description')


class InterventionType(models.Model):
    _name = 'intervention_type'
    _description = 'Intervention Type'

    name = fields.Char(string='Type', required=True)
    description = fields.Text(string='Description')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    equipment_category_id = fields.Many2one('maintenance.equipment.category', string='Equipment Category')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
    image = fields.Binary(string="Icon")  # Nouveau champ pour l'icône


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    intervention_type_ids = fields.Many2many('intervention_type', string='Intervention Types')


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.onchange('category_id')
    def _onchange_category_id(self):
        return {'domain': {'equipment_id': [('category_id', '=', self.category_id.id)]}}

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.intervention_type_ids = self.equipment_id.intervention_type_ids

    intervention_type_id = fields.Many2one(
        'intervention_type', string='Intervention Type'
    )
    equipment_category_id = fields.Many2one(
        'maintenance.equipment.category', string='Equipment Category', related='category_id'
    )
