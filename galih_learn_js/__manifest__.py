{
    'name': "Learn Javascript",

    'summary': """
         Learn Javascript 
        """,

    'author': "Port Cities",
    'website': "http://www.portcities.net",
    'version': '13.0.1.0.0',
    'depends': ['sale'],

    'data': [
        'views/assets.xml',
        'views/learn_js.xml',
        'security/ir.model.access.csv'
    ],

    'qweb':[
        'static/src/xml/view.xml'
    ],
    
    'auto_install': False,
    'installable': True,
    'application': True,
    'license': 'OEEL-1'
}
