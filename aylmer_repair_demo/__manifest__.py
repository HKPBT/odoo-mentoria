{
    "name": "Aylmer Repair Demo Website",
    "summary": "Site de démonstration Aylmer Repair intégré à Odoo Website",
    "version": "20.0.1.0.3",
    "category": "Website/Website",
    "license": "LGPL-3",
    "depends": [
        "website_sale",
        "sale_renting",
        "appointment",
        "helpdesk_repair",
        "repair",
    ],
    "data": [
        "views/website_assets.xml",
        "views/website_templates.xml",
        "views/website_menu.xml",
        "data/rental_inspection_sequence.xml",
        "security/ir.model.access.csv",
        "views/rental_inspection_views.xml",
    ],
    "installable": True,
    "application": True,
}
