# Aylmer Repair Website for Odoo 20

This addon gives the Aylmer Repair landing page a branded presentation while using Odoo's catalog and transactional pages for the actual shop. The home page shows published sale and rental products from the current Odoo database. The shop, product pages, cart, checkout, and rental date selection stay on Odoo's native eCommerce and Rental flows.

## Odoo apps

The addon depends on Website eCommerce (`website_sale`), Rental (`sale_renting`), Appointments (`appointment`), and Helpdesk/Repairs integration (`helpdesk_repair`). Odoo installs these dependencies with the addon; the required apps must be available in the database's Odoo edition and subscription.

## Configuration after installation

1. In **Website ‣ eCommerce ‣ Products**, create sale products, set their CAD prices, and publish them. Published products that are not rental products appear on the demo landing page and in `/shop`.
2. In **Rental**, create rental products, configure their rental price periods and pickup/return availability, then publish them on the website. Their cards appear on the landing page; customers open each product page to select dates and request a rental through Odoo.
3. Enable CAD in currencies, create/select the CAD pricelist for the website, and configure taxes and payment providers as required. The website uses Odoo's current website pricelist; the addon does not change company currency or payment settings.
4. In **Appointments**, create and publish a repair appointment type with the correct staff/resources and availability. The landing page links to the first published appointment type.
5. In **Helpdesk**, enable the Website Form on the repair team and set the website contact form's action/team to create Helpdesk tickets. Enable Repairs for that team. The standard `/contactus` form can then receive repair requests; staff can turn a ticket into a Repair Order from Helpdesk.

The `La démo Odoo` process panel remains a clearly labeled illustration. It does not create test transactions. All product browsing, sales orders, rental orders, date availability and appointment bookings use Odoo records and flows.

## Install on Odoo.sh

1. Push this branch to the Odoo.sh project and wait for the build to finish.
2. In the target database, open Apps, update the app list, and install or upgrade **Aylmer Repair Demo Website**.
3. Open `/aylmer-repair-demo`; shop and product details use `/shop` and the standard Odoo product URLs.
