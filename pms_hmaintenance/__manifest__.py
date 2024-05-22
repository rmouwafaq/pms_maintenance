{
    'name': 'PMS Hotel Maintenance',
    'version': '1.0',
    'author': 'odoo 17',
    'category': 'Maintenance',
    'depends': ['base','maintenance',],
    'data': [

        'security/ir.model.access.csv',
        'views/maintenance_request_views.xml',

        'security/security.xml',
        'views/maintenance_intervention_wizard_view.xml',
        'data/equipment_categories_data.xml',
        'data/equipment_data.xml',
        'data/hk_area_data.xml',
        'data/maintenance_team_data.xml',
        'data/intervention_type_data.xml',
        'data/maintenance_stage.xml',
        'views/pms_hmaintenance.xml',
        'views/assign_technician_wizard_views.xml',
        'views/view_maintenance_complete.xml',





    ],
    'installable': True,
}