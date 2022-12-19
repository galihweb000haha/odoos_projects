{
    'name': 'Helpdesk Merge Tickets',
    'summary': "Make two or more tickets can be merge ",
    'description': """
        v1.0.0
            * Create new transient model
            * Create wizard to show selected tickets
            * Create method to merge tickets
            By: Galih Fikran
    """,
    'author': "Port Cities",
    'website': "portcities.net",
    'version': '13.0.1.0.0', 
    'data': [
        'wizard/helpdesk_merge_ticket.xml'
    ],
    'depends': ['helpdesk'],
    'auto_install': False,
    'installable': True,
    'application': False,
    'license': 'OEEL-1'
}