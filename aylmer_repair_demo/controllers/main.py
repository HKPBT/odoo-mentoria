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
        Product = request.env["product.template"].with_context(
            website_id=request.website.id,
        )
        published = [
            ("website_published", "=", True),
            ("sale_ok", "=", True),
        ]
        rental_products = Product.search(
            published + [("rent_ok", "=", True)],
            limit=3,
            order="website_sequence, name",
        )
        sale_products = Product.search(
            published + [("rent_ok", "=", False)],
            limit=3,
            order="website_sequence, name",
        )
        appointment_type = request.env["appointment.type"].search(
            [("website_published", "=", True)],
            limit=1,
        )
        return request.render(
            "aylmer_repair_demo.website_demo_page",
            {
                "rental_products": rental_products,
                "sale_products": sale_products,
                "appointment_url": appointment_type.website_url
                if appointment_type
                else False,
            },
        )
