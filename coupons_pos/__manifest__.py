{
    'name': 'Coupons Point of Sale',
    'version': '13.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Manage Point of Sale Coupone',
    'description': """
        v1.0.0
        * new model named coupon.pos
        * coupon button to input coupon code
        * gift-coupon product will be added into orderlines
        * gift-coupon product will reduce the total amount
        By: Galih Fikran
    """,
    'author': 'Port Cities',
    'website': 'https://www.portcities.net',
    'company': 'Port Cities',
    'depends': ['point_of_sale'],
    'data': [
        'data/product_data.xml',
        'views/coupons_view.xml',
        'views/assets.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/coupons.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}