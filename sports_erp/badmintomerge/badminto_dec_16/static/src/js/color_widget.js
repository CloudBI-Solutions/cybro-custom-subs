odoo.define('color_widget', function (require) {
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
        this.totalColors = 11;
        this._super.apply(this, arguments);
    },
    _renderEdit: function () {
        this.$el.empty();
        var values = [0,10,20,30,40,50,60,70,80,90,100];
        var tooltip = [{'value': "0"}, {'value': "10"},
                       {'value': "20"}, {'value': "30"},
                       {'value': "40"}, {'value': "50"},
                       {'value': "60"}, {'value': "70"},
                       {'value': "80"}, {'value': "90"},
                       {'value': "100"}]
        for (var i = 0; i < this.totalColors; i++ ) {
            var className = "o_color_pill o_color_" + i;
            if (this.value === values[i] ) {
                className += ' active';
            }
            var elem = this.$el.append($('<span>', {
                'class': className,
                'data-val': values[i],
                'data-toggle': "tooltip",
                'data-placement': "top",
                'title': tooltip[i].value,
            }));
            elem[0].childNodes[i].append(i);
        }

    },
    _renderReadonly: function () {
        var val = 0;
        if (this.value == 10){val=1}
        else if (this.value == 20){val=2}
        else if (this.value == 30){val=3}
        else if (this.value == 40){val=4}
        else if (this.value == 50){val=5}
        else if (this.value == 60){val=6}
        else if (this.value == 70){val=7}
        else if (this.value == 80){val=8}
        else if (this.value == 90){val=9}
        else if (this.value == 100){val=10}
        var className = "o_color_pill active readonly o_color_" + val;
        this.$el.append($('<span>', {
            'class': className,
        }));
        this.$el.children().append('<span class="o_inner_text">'+val+'</span>');

    },

    clickPill: function (ev) {
        var $target = $(ev.currentTarget);
        var data = $target.data();
        if (this.mode == 'edit'){
            this._setValue(data.val.toString());
        }
    }
});

fieldRegistry.add('badminto_color', colorField);

return {
    colorField: colorField,
};
});