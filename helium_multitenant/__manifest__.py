# -*- coding: utf-8 -*-
{
    'name': "Helium Multitenant",
    'summary': """""",
    'description': """
        Support multitenant features in Bahmni Odoo
    """,
    'author': "IntelliSOFT Kenya",
    'website': "https://intellisoftkenya.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Insurance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ["base", "sale", "account"],

    # always loaded
    'data': [
        'views/pricelist.xml',
        'views/sale_order.xml',
        'views/warehouse.xml',
        'security/security.xml'
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #    'demo.xml',
    # ],
    'Installable': True,
    'auto_install': False,
    'application': True
}
