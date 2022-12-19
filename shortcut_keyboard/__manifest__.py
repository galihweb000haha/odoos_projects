{
    'name': "Galih Shortcut Keyboard",
    'version': '13.0.0.1.0',

    'description': """
         This extra tool will show new item in action button from transfer page called merge pick, this feature can merge some picking or delivery order
        """,

    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'depends': ['point_of_sale'],

    'data': [
        'views/assets.xml',
        'views/pos_shortcut_config_view.xml',
        'views/account_journal_view.xml',
        'security/ir.model.access.csv'
    ],

    'qweb': ['static/src/xml/pos.xml'],
    
    'auto_install': False,
    'installable': True,
    'application': False,
    'license': 'OEEL-1'
}
