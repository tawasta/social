/** @odoo-module **/

//import { Link } from "@website_editor/js/wysiwyg/widgets/link";
import { LinkDialog} from "@web_editor/js/wysiwyg/widgets/link_dialog";
import { LinkTools } from "@web_editor/js/wysiwyg/widgets/link_tools";
import { Link } from "@web_editor/js/wysiwyg/widgets/link";
import { patch } from "@web/core/utils/patch"

patch(LinkDialog.prototype, {
    _doStripDomain() {
        return false;
    }
});

patch(LinkTools.prototype, {
    _doStripDomain() {
        return false;
    }
});

patch(Link.prototype, {
    _doStripDomain() {
        return false;
    }
});

