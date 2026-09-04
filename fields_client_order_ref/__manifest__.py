{
    'name': 'Onchange field client_order_ref',
    'version': '19.0.0.1',
    'summary': 'Ensures client_order_ref is updated across related records.',
    'description': '''
This module ensures that the client_order_ref field is consistently updated across related records in the sale.order,
stock.picking, and account.move models. It includes a post-installation hook to update existing records and modifies
views to display the client_order_ref field.    
''',
    'license': 'OPL-1',
    'category': 'All',
    'author': 'Blanco Martín & Asociados',
    'website': 'http://blancomartin.cl',
    'depends': ['stock', 'account', 'sale_management'],
    'installable': True,
    'data': [
        'views/picking.xml'
    ],
    'post_init_hook': '_update_client_order_ref',
}
