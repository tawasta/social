from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PartnerMailListWizard(models.TransientModel):
    _name = "op.competence.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list_id = fields.Many2one(
        comodel_name="mail.mass_mailing.list", string="Mailing List"
    )
    competence_ids = fields.Many2many(
        comodel_name="op.competence",
        relation="mail_list_wizard_competence",
        default=lambda self: self.env.context.get("active_ids"),
    )

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env["mail.mass_mailing.contact"]
        competences = self.competence_ids

        add_list = competences.filtered("partner_id.mass_mailing_contact_ids")
        for competence in add_list:
            competence.partner_id.mass_mailing_contact_ids[
                0
            ].list_ids |= self.mail_list_id

        to_create = competences - add_list
        for competence in to_create:
            if not competence.partner_id.email:
                raise UserError(
                    _("Partner '%s' has no email.") % competence.partner_id.name
                )
            contact_vals = {
                "partner_id": competence.partner_id.id,
                "list_ids": [[6, 0, [self.mail_list_id.id]]],
                "title_id": competence.partner_id.title or False,
                "company_name": competence.partner_id.company_id.name or False,
                "country_id": competence.partner_id.country_id or False,
                "tag_ids": competence.partner_id.category_id or False,
            }
            contact_obj.create(contact_vals)
