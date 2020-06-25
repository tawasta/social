/*
odoo.define('mail_chatter_colors', function (require) {
    "use strict";

    var core = require('web.core');
    var time = require('web.time');

    $(function() {
        var colorChatter = function() {
            setTimeout(function() {
                const elems = $("p.o_mail_info");
                if(elems.length === 0) {
                    colorChatter();
                } else {
                    elems.values.forEach(function(elem) {
                        console.log(elem);
                    });
                }
            }, 1500);
        }

        $(document).ready(function() {
            colorChatter();
        });

    });
});
*/
