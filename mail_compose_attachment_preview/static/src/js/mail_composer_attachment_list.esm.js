import {MailComposerAttachmentList} from "@mail/core/web/mail_composer_attachment_list";
import {patch} from "@web/core/utils/patch";

patch(MailComposerAttachmentList.prototype, {
  getUrl(id) {
    // Without "?download=true" the browser opens the file instead of saving it
    return "/web/content/" + id;
  },
});
