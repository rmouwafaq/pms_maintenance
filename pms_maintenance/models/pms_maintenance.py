# -*- coding: utf-8 -*-

import ast
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.osv import expression

CLEAN_STATES = [('dirty', 'Dirty'),
                ('inspect', 'Inspect'),
                ('clean', 'Clean'),

                ]

PMS_ROOM_HK_STATE = [('vacant', 'Vacant'),
                     ('occupied', 'Occupied'),
                     ('blocked', 'Blocked'),
                     ]


class PmsHkArea(models.Model):
    _name = 'pms.hk.area'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Housekeeping Area'

    name = fields.Char('Name', tracking=True)
    active = fields.Boolean('Active', default=True, tracking=True)
    clean_state = fields.Selection(CLEAN_STATES, 'Status', default='clean')
    hk_state = fields.Selection(PMS_ROOM_HK_STATE, string="HK Status", default='vacant')
    hk_pax = fields.Integer(string="Control PAX")
    color = fields.Integer('Color', default=0)
    request_ids = fields.One2many('maintenance.request','hk_area_id',string='Requests')


class PmsHkRequestType(models.Model):
    _name = 'pms.hk.request.type'

    name = fields.Char('Subjects', required=True)
    category_id = fields.Many2one('maintenance.equipment.category', string='Category')
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    maintenance_team_id = fields.Many2one('maintenance.team', string='Team', required=True)
    description = fields.Html('Description')
    duration = fields.Float(help="Duration in hours.")
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    color = fields.Integer('Color Index')
    # bloque la chambre ?
    # pour quel type hébergement

class MaintenanceRequest(models.Model):

    _inherit = 'maintenance.request'

    hk_area_id = fields.Many2one('pms.hk.area', string='Hk Area',required=True)
