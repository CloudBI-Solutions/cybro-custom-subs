odoo.define('badminto.add_button', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.AddButton = publicWidget.Widget.extend({
        selector: '.badminto-dropdown',
        events: {
            'click #add_assessment_type': '_onAddAssessmentTypeClicked',
            },
        _onAddAssessmentTypeClicked: function (ev) {
            console.log('clicked');
            var checkedElements = this.$el.find('input[type="checkbox"]:checked');
            var checkedElementsValue = []
            if (checkedElements.length > 0) {
                for (var i = 0; i < checkedElements.length; i++)
                {
                    checkedElementsValue.push(checkedElements[i].defaultValue)
                }
            }
            console.log(checkedElementsValue);
            var assessmentField = document.getElementById('assessment_types');
            ajax.jsonRpc('/assessment_field_value', 'call',{'assessment_ids': checkedElementsValue})
            .then(function (result) {
                console.log(result);
                var res = $('#assessment_types');
                res.select2();
                for (var i=0; i < result.length; i++){
                    var newOption = new Option(result[i].name, result[i].id, true, true);
                     res.append(newOption).trigger('change');
                }
            });
        }
    });

});