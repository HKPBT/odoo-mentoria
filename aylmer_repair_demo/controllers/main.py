from odoo import http
from odoo.http import request


class AylmerRepairDemoController(http.Controller):
    @http.route(
        "/aylmer-repair-demo",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def aylmer_repair_demo(self, **kwargs):
        return request.render("aylmer_repair_demo.website_demo_page")
