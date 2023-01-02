odoo.define('sports_erp_dashboard.tree_view_select', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');

    publicWidget.registry.TreeViewSelect = publicWidget.Widget.extend({
        selector: '.get-values__list',
        events: {
        'click th > .set-input--checkbox': '_onSelectAll',
        'click #assign-button': '_onAssign'

        },
        _onSelectAll: function (ev) {
            var checkbox_header = document.getElementById('select-all');
            if (checkbox_header.checked) {
                var checkbox = document.getElementsByName('select');
                if (checkbox.length > 0){
                    console.log('checked', checkbox);
                    for (var i = 0; i < checkbox.length; i++) {
                        checkbox[i].checked = true;
                    }
                }
            }
            else
            {
                var checkbox = document.getElementsByName('select');
                if (checkbox.length > 0){
                    console.log('checked', checkbox);
                    for (var i = 0; i < checkbox.length; i++) {
                        checkbox[i].checked = false;
                    }
                }
            }
        },

        _onAssign : function (ev) {
            var checkbox = document.getElementsByName('select');
            var selector = document.getElementById('assigned');
            if (selector) {
                selector.innerHTML = '';
            }
            var attendees = document.getElementById('attendees_id');
            if (attendees) {
                attendees.innerHTML = '';
            }
            var members = document.getElementById('members_id');
            if (members) {
                members.innerHTML = '';
            }
            if (checkbox.length > 0){
                for (var i = 0; i < checkbox.length; i++) {
                    if(checkbox[i].checked == true){
                        console.log(document.getElementById(checkbox[i].value).value);
                        var res = $('#assigned');
                        res.select2();
                        var newOption = new Option(document.getElementById(checkbox[i].value).value,
                        checkbox[i].value, true, true);
                        res.append(newOption).trigger('change');

                        var res2 = $('#attendees_id');
                        res2.select2();
                        var newOption2 = new Option(document.getElementById(checkbox[i].value).value,
                        checkbox[i].value, true, true);
                        res2.append(newOption2).trigger('change');

                        var res3 = $('#members_id');
                        res3.select2();
                        var newOption3 = new Option(document.getElementById(checkbox[i].value).value,
                        checkbox[i].value, true, true);
                        res3.append(newOption3).trigger('change');
                    }
                }
            }
        },

    });
});