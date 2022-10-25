odoo.define("mail_highlight/static/src/models/message.js", function (require) {
    "use strict";
    const {
        registerClassPatchModel,
        registerFieldPatchModel,
    } = require("mail/static/src/model/model_core.js");
    const {attr} = require("mail/static/src/model/model_field.js");
    registerClassPatchModel(
        "mail.message",
        "/mail_highlight/static/src/models/message.js",
        {
            /**
             * @override
             */
            convertData(data) {
                const data2 = this._super(data);
                if ("is_highlight" in data) {
                    data2.is_highlight = data.is_highlight;
                }
                return data2;
            },
        }
    );
    registerFieldPatchModel(
        "mail.message",
        "mail_highlight/static/src/models/message.js",
        {
            is_highlight: attr({
                default: false,
            }),
        }
    );
});
