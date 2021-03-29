from odoo import _, api, models
from odoo.exceptions import UserError


class PartnerMailListWizard(models.TransientModel):
    _inherit = "partner.mail.list.wizard"
    _description = "Create contact mailing list"

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env['mail.mass_mailing.contact']
        partners = self.partner_ids
        user_data = []
        mail_list_contacts = self.mail_list_id.contact_ids.mapped("partner_id")
        for partner in partners:
            if partner.id not in mail_list_contacts.ids:
                if partner.email not in user_data:
                    if not partner.email:
                        raise UserError(
                            _("Partner '%s' has no email.") % partner.name
                        )
                    contact_vals = {
                        'partner_id': partner.id,
                        'list_ids': [[6, 0, [self.mail_list_id.id]]],
                        'title_id': partner.title or False,
                        'company_name': partner.company_id.name or False,
                        'country_id': partner.country_id or False,
                        'tag_ids': partner.category_id or False,
                    }
                    contact_obj.create(contact_vals)
                    user_data.append(partner.email)
