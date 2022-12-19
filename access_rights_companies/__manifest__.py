{
    'name': "Access Right Company",
    'summary': "create feature to print card for specific employee with show the barcode",
    'description': """
        v0.1.0
        * create menu item that can print employee card.
        * employee card will be print in portrait mode of paper format (55mm X 90mm).
        * generate the barcode of the employee.
        * create new menu item that used to scan the barcode.
        * scan page will get the barcode from barcode scanner, if barcode is valid then user will be redirect to specific employee page based on barcode.
        By: Galih Fikran
    """,

    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'version': '13.0.1.0.0',
    'depends': ['purchase'],

    'data': [
        'security/security.xml',
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'data/res_company_data.xml'
    ],

    'auto_install': False,
    'installable': True,
    'application': False,
    'license': 'OEEL-1'
}
