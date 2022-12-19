{
    'name': 'Midtrans Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'version': '13.0.0.1.0',
    'sequence': 343,
    'summary': 'Payment Acquirer: Midtrans Implementation',
    'description': """
        v0.1.0
        * adding midtrans payment acquirer
        * integration payment with snap
        By:Galih Fikran
    """,
    'author': 'Port Cities',
    'website': "http://www.portcities.net",
    'depends': ['payment'],
    'data': [
        'views/midtrans_view.xml',
        'data/payment_acquirer_data.xml',
        'views/assets.xml',
    ],
    'application': False,
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
    'external_dependencies': {"python" : ["midtransclient"]}
}
