odoo.define('mass_editor.basic_model', function (require) {
"use strict";
var BasicModel = require('web.BasicModel');

BasicModel.include({
    _parseServerData: function (fieldNames, element, data)
    {
        var self = this;
        _.each(fieldNames, function (fieldName) {
            var field = element.fields[fieldName];
            var val = data[fieldName];
            if (field.type === 'many2one') {
                if (val) {
                    var r = self._makeDataPoint({
                        modelName: field.relation,
                        fields: {
                            display_name: {type: 'char'},
                            id: {type: 'integer'},
                        },
                        data: {
                            display_name: val[1],
                            id: val[0],
                        },
                        parentID: element.id,
                    });
                    data[fieldName] = r.id;
                }
                else {
                    data[fieldName] = false;
                }
            }
            else {
                data[fieldName] = self._parseServerValue(field, val);
                }
            });
        }
    });
});
