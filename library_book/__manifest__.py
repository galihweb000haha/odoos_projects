{
    'name': "Library Book",

    'summary': """
         Library Book 
        """,

    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'version': '13.0.1.0.0',
    'depends': ['base'],

    'data': [
        'data/library_book.xml',
        'security/ir.model.access.csv',
        'views/library_book_view.xml',
        'views/books_view.xml',
        'views/guest_book_view.xml',
        'views/member_view.xml'
    ],
    
    'auto_install': False,
    'installable': True,
    'application': True,
    'license': 'OEEL-1'
}
