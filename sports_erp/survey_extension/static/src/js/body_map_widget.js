odoo.define('survey_extension.survey_body_map_extension', function (require) {
    "use strict";

var core = require('web.core');
var QWeb = core.qweb;
var field_utils = require("web.field_utils")
var session = require('web.session');
var rpc = require('web.rpc')
var widgetRegistry = require('web.widget_registry');
var Widget = require('web.Widget');

var body_map = Widget.extend({
	template: 'body_map_view',
	events:{
        'click .newcircle': 'onClickCircle',
        'click #btnDanger': 'onClickCancel',
    },
	 init: function (parent, action) {
        this._super.apply(this, arguments);
    },
    start: function () {
        var self = this;
        var NS = 'http://www.w3.org/2000/svg'


        for(var i=0;i<this.__parentedParent.state.data.value_body_map.data.length;i++){

            var x_value = this.__parentedParent.state.data.value_body_map.data[i].data.x_value
            var y_value =this.__parentedParent.state.data.value_body_map.data[i].data.y_value
            var newCircIdParam = "newcircle" + x_value + '-' + y_value
            var circle = document.createElementNS(NS, 'circle');
            circle.setAttributeNS(null, 'cx', x_value);
            circle.setAttributeNS(null, 'cy', y_value);
            circle.setAttributeNS(null, 'r', 10);
            circle.setAttributeNS(null, 'class', "newcircle");
            circle.setAttributeNS(null, 'id', newCircIdParam);
            circle.setAttributeNS(null, 'data-x', x_value);
            circle.setAttributeNS(null, 'data-y', y_value);
            $(self.el).find('#humanInner').after(circle)
        }
    },
    onClickCircle(e){
        var pinForm = $(this.el).find('#pinForm');
        rpc.query({
                    model: 'survey.body.map.value',
                    method: 'search_read',
                    args: [[['x_value','=',$(e.target).data('x')],['y_value','=',$(e.target).data('y')]]],
                }).then(function (res){
//                    if(res[0]['name']){
//                        $('#name').val(res[0]['name']);
//                    }
                    if(res[0]['pain_level']){
                        $('#pain_level').val(res[0]['pain_level']);
                    }
//                    if(res[0]['mark_area']){
//                        $('#mark_area').val(res[0]['mark_area']);
//                    }
                    if(res[0]['comment']){
                        $('#Comment').val(res[0]['comment']);
                    }
                    pinForm.show();
                });
    },
    onClickCancel(e){
        var pinForm = $(this.el).find('#pinForm');
        pinForm.hide();
    }
});

widgetRegistry.add("body_map", body_map)

});