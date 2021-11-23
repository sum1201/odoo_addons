{
    "name": "Survey Qrcode URL",
    "version": "1.0",
    'author': '山西清水欧度信息技术有限公司',
    'website': 'https://www.odooqs.com',
    "category": "survey",
    'summary': 'survey',
    'description': """
    """,
    'license': 'OPL-1',
    'depends': ['survey'],
    "init_xml": [],
    "data": [
        'security/ir.model.access.csv',
        'wizards/survey_result_wizard_view.xml',
        'views/survey_views.xml',
        'views/assets.xml'
    ],
    'demo_xml': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'active': False
}
