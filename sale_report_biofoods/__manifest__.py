{
    'name': 'Sale Report Biofoods',
    'version': '17.0.1.0.0',
    'summary': 'Agrega Campos al Reporte de Ventas',
    'description': '''Margen Neto, Precio Unitario, Costo Unitario, Acuerdos Comerciales %
        Acuerdos Comerciales %: Campo definido en el Contacto, representa un porcentaje de la venta que cobra un retail 
        por vender el producto. Al confirmar una Orden de Venta, se guarda el valor actual de Acuerdos Comerciales %
        definido en el Contacto en ella para mantener el valor en caso de que se modifique en el futuro.''',
    'license': 'OPL-1',
    'category': 'Sale',
    "author": "Blanco Martín & Asociados",
    'depends': ['sale_margin'],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
}
