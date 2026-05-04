/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { Link } from "@web_editor/js/wysiwyg/widgets/link";

export class LinkDialog extends Link {
    /**
     * @override
     */
    _doStripDomain() {
        return false;
    }
}
