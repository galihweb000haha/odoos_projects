{
    'name': 'Basic Point Of Sale',
    'summary': 'The new configurable Odoo Web Login Screen',
    'version': '13.0.1.0',
    'category': 'Website',
    'description': """
        v0.1.0
        * Nanannana
    """,
    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'point_of_sale'
    ],
    'data': [
        'views/assets.xml',
        'views/pos_order_view.xml',
        'views/report_pos_order.xml',
    ],
    'qweb': [
        'static/src/xml/chrome_view.xml',
    ],
    'installable': True,
    'application': False
}
