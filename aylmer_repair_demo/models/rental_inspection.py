from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AylmerRentalInspection(models.Model):
    _name = "aylmer.rental.inspection"
    _description = "Rental equipment check-in/check-out inspection"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "inspection_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(
        string="Référence",
        required=True,
        copy=False,
        default="/",
        tracking=True,
    )
    phase = fields.Selection(
        [("pickup", "Sortie / remise au client"), ("return", "Retour du matériel")],
        string="Étape",
        required=True,
        default="pickup",
        tracking=True,
    )
    state = fields.Selection(
        [("draft", "À compléter"), ("done", "Validé")],
        string="Statut",
        default="draft",
        required=True,
        tracking=True,
    )
    inspection_date = fields.Datetime(
        string="Date du contrôle", default=fields.Datetime.now, required=True
    )
    inspector_id = fields.Many2one(
        "res.users", string="Technicien", default=lambda self: self.env.user, required=True
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    rental_order_id = fields.Many2one(
        "sale.order", string="Commande de location", required=True, ondelete="cascade",
        index=True, tracking=True,
    )
    customer_id = fields.Many2one(
        "res.partner", string="Client", related="rental_order_id.partner_id", store=True
    )
    rental_order_line_id = fields.Many2one(
        "sale.order.line",
        string="Ligne de location",
        required=True,
        domain="[('order_id', '=', rental_order_id), ('product_id.product_tmpl_id.rent_ok', '=', True)]",
    )
    product_id = fields.Many2one(
        "product.product", string="Matériel", related="rental_order_line_id.product_id", store=True
    )
    serial_id = fields.Many2one(
        "stock.lot",
        string="Numéro de série / lot",
        domain="[('product_id', '=', product_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        tracking=True,
    )
    return_picking_id = fields.Many2one(
        "stock.picking",
        string="Transfert de retour Odoo",
        domain="[('return_id', '!=', False), ('partner_id', '=', customer_id)]",
        help="Associez le transfert de retour validé dans Inventaire. Il permet de créer la réparation au nom du client.",
    )

    visual_condition_ok = fields.Boolean(string="État visuel vérifié")
    starts_ok = fields.Boolean(string="Démarrage vérifié")
    safety_ok = fields.Boolean(string="Protections et sécurité vérifiées")
    accessories_ok = fields.Boolean(string="Accessoires vérifiés")
    clean_ok = fields.Boolean(string="Matériel propre")
    fuel_level = fields.Selection(
        [("empty", "Vide"), ("quarter", "¼"), ("half", "½"), ("three_quarters", "¾"), ("full", "Plein")],
        string="Niveau de carburant",
    )
    meter_reading = fields.Float(string="Lecture du compteur", digits=(12, 1))
    damage_found = fields.Boolean(string="Dommage ou anomalie constaté", tracking=True)
    damage_notes = fields.Text(string="Dommages, pièces manquantes ou observations")
    photo_ids = fields.Many2many(
        "ir.attachment", "aylmer_inspection_attachment_rel", "inspection_id", "attachment_id",
        string="Photos du matériel",
        help="Ajoutez les photos prises au départ ou au retour.",
    )
    customer_signature = fields.Binary(string="Signature du client", attachment=True)
    inspector_signature = fields.Binary(string="Signature du technicien", attachment=True)
    repair_id = fields.Many2one("repair.order", string="Ordre de réparation", readonly=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals["name"] == "/":
                vals["name"] = self.env["ir.sequence"].next_by_code("aylmer.rental.inspection") or _("Nouveau contrôle")
        return super().create(vals_list)

    @api.constrains("rental_order_id", "rental_order_line_id", "serial_id")
    def _check_rental_line(self):
        for inspection in self:
            line = inspection.rental_order_line_id
            if line and (line.order_id != inspection.rental_order_id or not line.product_id.product_tmpl_id.rent_ok):
                raise ValidationError(_("La ligne sélectionnée doit être un produit de location de cette commande."))
            if inspection.serial_id and inspection.serial_id.product_id != inspection.product_id:
                raise ValidationError(_("Le numéro de série doit appartenir au matériel sélectionné."))

    def action_validate(self):
        for inspection in self:
            if inspection.product_id.tracking == "serial" and not inspection.serial_id:
                raise UserError(_("Sélectionnez le numéro de série de l’équipement avant de valider le contrôle."))
            if inspection.damage_found and not inspection.damage_notes:
                raise UserError(_("Décrivez le dommage ou l’anomalie avant de valider le contrôle."))
        self.write({"state": "done"})
        return True

    def action_reset_to_draft(self):
        self.write({"state": "draft"})
        return True

    def action_create_repair(self):
        self.ensure_one()
        if self.phase != "return":
            raise UserError(_("Un ordre de réparation peut être créé à partir du contrôle de retour."))
        if not self.damage_found:
            raise UserError(_("Cochez d’abord « Dommage ou anomalie constaté »."))
        if not self.return_picking_id:
            raise UserError(_("Associez le transfert de retour validé dans Inventaire pour reprendre le client et le matériel."))
        if self.return_picking_id.partner_id.commercial_partner_id != self.customer_id.commercial_partner_id:
            raise UserError(_("Le client du transfert de retour doit correspondre au client de la location."))
        if self.return_picking_id.return_id not in self.rental_order_id.picking_ids:
            raise UserError(_("Le transfert de retour sélectionné ne provient pas de cette commande de location."))
        if self.product_id not in self.return_picking_id.move_ids.product_id:
            raise UserError(_("Le matériel de la fiche ne figure pas sur le transfert de retour sélectionné."))
        if self.serial_id and self.serial_id not in self.return_picking_id.move_line_ids.lot_id:
            raise UserError(_("Le numéro de série de la fiche ne figure pas sur le transfert de retour sélectionné."))
        if self.repair_id:
            return self._open_repair()

        repair = self.env["repair.order"].create({
            "picking_id": self.return_picking_id.id,
            "product_id": self.product_id.id,
            "lot_id": self.serial_id.id or False,
            "sale_order_id": self.rental_order_id.id,
        })
        repair.partner_id = self.customer_id
        repair.message_post(body=_("Créé depuis la fiche de contrôle de location %(inspection)s.") % {
            "inspection": self.name,
        })
        self.repair_id = repair
        self.message_post(body=_("Ordre de réparation %(repair)s créé pour %(customer)s.") % {
            "repair": repair.display_name,
            "customer": self.customer_id.display_name,
        })
        return self._open_repair()

    def _open_repair(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Ordre de réparation"),
            "res_model": "repair.order",
            "view_mode": "form",
            "res_id": self.repair_id.id,
            "target": "current",
        }


class SaleOrder(models.Model):
    _inherit = "sale.order"

    aylmer_inspection_ids = fields.One2many(
        "aylmer.rental.inspection", "rental_order_id", string="Fiches de contrôle"
    )
    aylmer_inspection_count = fields.Integer(
        string="Fiches de contrôle", compute="_compute_aylmer_inspection_count"
    )

    @api.depends("aylmer_inspection_ids")
    def _compute_aylmer_inspection_count(self):
        for order in self:
            order.aylmer_inspection_count = len(order.aylmer_inspection_ids)

    def _action_new_rental_inspection(self, phase):
        self.ensure_one()
        if not self.order_line.filtered(lambda line: line.product_id.product_tmpl_id.rent_ok):
            raise UserError(_("Cette commande ne contient aucun produit configuré pour la location."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Fiche de contrôle — %s") % ("Sortie" if phase == "pickup" else "Retour"),
            "res_model": "aylmer.rental.inspection",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_rental_order_id": self.id,
                "default_phase": phase,
                "default_company_id": self.company_id.id,
            },
        }

    def action_new_pickup_inspection(self):
        return self._action_new_rental_inspection("pickup")

    def action_new_return_inspection(self):
        return self._action_new_rental_inspection("return")
