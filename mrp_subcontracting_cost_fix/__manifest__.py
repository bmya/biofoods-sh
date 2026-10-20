{
    'name': 'Fix Subcontracting Cost',
    'version': '19.0.1.1',
    'description': '''
Fix not considering the subcontracting cost when marking a manufacturing order as done.
Previosly it only worked correctly if you confirmed it from the picking.''',
    'license': 'OPL-1',
    'category': 'MRP',
    "author": "Blanco Martín & Asociados",
    'website': 'http://blancomartin.cl',
    'depends': ['mrp_subcontracting_account'],
    'installable': True,
}
