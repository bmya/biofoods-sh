{
    'name': 'Shopify Extended',
    'version': '17.0.0.1',
    'category': 'Sales',
    'summary': 'Modifications in shopify to Biofood',
    'license': 'OPL-1',
    "author": "Blanco Martín & Asociados",
    "website": "http://blancomartin.cl",
    'depends': [
        'common_connector_library',
        'shopify_ept'
    ],
    'data': [
        'views/product_template.xml',
        'views/product_view.xml',
        'wizard/basic_configuration_onboarding.xml'
    ],
    'installable': True,
}
