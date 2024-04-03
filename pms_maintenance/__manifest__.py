# -*- coding: utf-8 -*-

{
    'name': 'PMS Maintenance',
    'version': '1.0',
    'sequence': 1,
    'category': 'Property Management',
    'description': """
Management of maintenance requests within hospitality properties""",
    'depends': ['maintenance'],
    'summary': 'Management of maintenance requests within hospitality properties',
    'website': 'https://www.agilorg.com',
    'data': [
        'security/pms_maintenance.xml',
        'security/ir.model.access.csv',
        'data/maintenance_data.xml',
        'views/hk_area_maintenance_view.xml',
        'views/hk_request_type_view.xml',
        'views/pms_maintenance_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
