from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PartnerMailListWizard(models.TransientModel):
    _name = "op.student.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list_id = fields.Many2one(comodel_name="mail.mass_mailing.list",
                                   string="Mailing List")
    student_ids = fields.Many2many(
        comodel_name="op.student", relation="mail_list_wizard_student",
        default=lambda self: self.env.context.get("active_ids"))

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env['mail.mass_mailing.contact']
        students = self.student_ids

        print("===========================")
        print(students)
        print("===========================")

        add_list = students.filtered('mass_mailing_contact_ids')
        for student in add_list:
            student.partner_id.mass_mailing_contact_ids[0].list_ids |= self.mail_list_id

        to_create = students - add_list
        for student in to_create:
            if not student.partner_id.email:
                raise UserError(_("Partner '%s' has no email.") % student.partner_id.name)
            contact_vals = {
                'partner_id': student.partner_id.id,
                'list_ids': [[6, 0, [self.mail_list_id.id]]],
                'title_id': student.partner_id.title or False,
                'company_name': student.partner_id.company_id.name or False,
                'country_id': student.partner_id.country_id or False,
                'tag_ids': student.partner_id.category_id or False,
            }
            contact_obj.create(contact_vals)
