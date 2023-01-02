odoo.define('mass_editor.mass_edit_button', function (require) {
    "use strict";
    console.log("haaaaaaaaai")

    var core = require('web.core');
    var ListView = require('web.ListView');
    var ListController = require("web.ListController");
    var records = []
    console.log("haaaaaaaaaaai")

    var includeEdit = {

        _onSelectionChanged: function (event) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                records = this.getSelectedIds();
                if (records.length > 0) {
                    this.$buttons.find('button.o_edit_btn').show();
                }
                else{
                    this.$buttons.find('button.o_edit_btn').hide();
                }
            }
        },

        renderButtons: function() {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('button.o_edit_btn').hide();
                var mass_edit_btn = this.$buttons.find('button.o_edit_btn');
                mass_edit_btn.click(this.proxy('_mass_edit_option'));
            }
        },

        _mass_edit_option: function() {
            var action = {
                type: "ir.actions.act_window",
                name: "Mass Editor",
                res_model: "mass.editor.wizard",
                views: [[false,'form']],
                target: 'new',
                view_type : 'form',
                view_mode : 'form',
                context : {'active_model': this.modelName,
                           'selected_records': records},
                flags: {'form': {'action_buttons': true, 'options': {'mode': 'edit'}}}
            }
            return this.do_action(action);
        },
    }
    ListController.include(includeEdit);
});
