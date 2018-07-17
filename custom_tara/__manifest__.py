{
    'name': "Addons Tarakusuma",
    'summary': """
        Customization for Tarakusuma""",

    'description': """\

Customization for Tarakusuma
============================

* Credit limit each customer
* Customization address for shipping and delivery
* Discount header level on form sales order and invoices
* Customization for e-faktur to get discount level
* Bank transfer selection on invoice
* Approval selection on invoice
* Update format delivery slip
* Update format invoice slip
    """,

    'author': "Yohanes Ho",
    'website': "",
    'category': 'Tarakusuma Addon',
    'version': '0.1',

    'depends': [
        'base', 
        'account', 
        'sale',
        'stock',
        'vit_efaktur',
    ],

    'data': [
        'security/custom_security.xml',
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/account_invoice_view.xml',
        'views/res_bank_view.xml',
        'views/stock_view.xml',
        'views/currency_view.xml',
        'reports/report_deliveryslip.xml',
        'reports/report_invoice.xml',
        'reports/custom_paper.xml',
        'reports/report_external_header.xml',
    ],

    'demo': [
    ],
    "application": True,
	"installable": True,
    "auto_install": False,
}