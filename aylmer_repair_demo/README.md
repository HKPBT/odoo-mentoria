# Aylmer Repair Demo Website (Odoo 20.0)

Installable Odoo Website addon for Odoo 20.0. It adds the public route `/aylmer-repair-demo`, registers it in the Website menu, and loads this prototype's CSS and JavaScript only on that route. It uses Odoo's website layout, language/website routing, session and publishing infrastructure.

## Install

1. Add this directory (`aylmer_repair_demo`) to the addons path used by the Odoo.sh branch.
2. Rebuild/restart the branch, then sign in as a website administrator.
3. In Apps, update the app list and install **Aylmer Repair Demo Website**.
4. Open `/fr/aylmer-repair-demo` (or `/en/aylmer-repair-demo`) and publish it if required. The module adds an **Aylmer Repair** item to the site menu.

The Odoo instance provided for this task is Odoo 20.0. Its URL identifies the Odoo.sh branch as `develop`, while this code is being prepared on repository branch `dev`. The add-on has not been deployed or installed: this workspace has no authenticated administrator session for the database, and the target branch needs to be confirmed. No Odoo site content has been changed.

The rental availability, special-order and repair scenario cards remain explicit simulations. They do not create rental orders, repair orders, sales orders, deposits or stock moves in Odoo. Actual transactional integration requires the relevant Odoo apps and confirmed business rules/data. The existing `/shop` and `/contactus` pages remain available on the same Odoo Website.
