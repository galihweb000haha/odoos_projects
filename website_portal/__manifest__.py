{
    'name': "Website Portal",
    'summary': "adjustment sale order portal, add new portal named Sale Order: To Invoice",
    'description': """
        v0.1.0
         * add customer field in sale order portal.
         * add customer field in sale order detail after order date field.
         * create new menu item in report menu to print excel report.
         * create new button named confirm quotation above print button in sale order detail to confirm sale order where state is quotation.
         * add new portal named Sale Orders: To invoice, it contain sale order where state is to invoice or invoiceable.
         * Add a sort by, filter by, and group by in sale order portal.
         By: Galih Fikran
    """,

    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'version': '13.0.0.1.0',
    'depends': ['website', 'sale'],

    'data': [
        'views/website_portal_view.xml'
    ],
    
    'auto_install': False,
    'installable': True,
    'application': False,
    'license': 'OEEL-1'
}
