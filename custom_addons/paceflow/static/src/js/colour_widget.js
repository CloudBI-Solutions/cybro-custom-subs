odoo.define('colour_widget', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var fieldRegistry = require('web.field_registry');

var colorField = AbstractField.extend({
    className: 'o_int_colorpicker',
    tagName: 'span',
    supportedFieldTypes: ['integer'],
    events: {
        'click .o_color_pill': 'clickPill',
    },
    init: function () {
        this.totalColors = 4;
        this._super.apply(this, arguments);
    },
    _renderEdit: function () {
        this.$el.empty();
        var values = [0,33,66,100];
        var tooltip = [{'value': "Nil"}, {'value': "Green"}, {'value': "Amber"}, {'value': "Red"}]
        for (var i = 0; i < this.totalColors; i++ ) {
            console.log(values[i])
            var className = "o_color_pill o_color_" + i;
            if (this.value === values[i] ) {
                className += ' active';
            }
            this.$el.append($('<span>', {
                'class': className,
                'data-val': values[i],
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': tooltip[i].value,
            }));
        }
    },
    _renderReadonly: function () {
        var val = 0;
        if (this.value == 33){val=1}
        else if (this.value == 66){val=2}
        else if (this.value == 100){val=3}
        var className = "o_color_pill active readonly o_color_" + val;
        this.$el.append($('<span>', {
            'class': className,
        }));
    },
    clickPill: function (ev) {
        var $target = $(ev.currentTarget);
        var data = $target.data();
        this._setValue(data.val.toString());
    }

});

fieldRegistry.add('int_color', colorField);

return {
    colorField: colorField,
};
});