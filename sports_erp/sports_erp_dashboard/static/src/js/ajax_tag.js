odoo.define('sports_erp_dashboard.ajax_tag', function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.AjaxTag = publicWidget.Widget.extend({
        selector: '.addTagModal',
        events: {
            'click #add_discipline_tag': '_onAddDisciplineTag',
            'click #add_fan_tag': '_onAddFanTag',
            'click #add_athlete_tag': '_onAddAthleteTag',
            'click #add_coach_tag': '_onAddCoachTag',
            'click #add_venues_tag': '_onAddVenueTag',
            'click #add_parents_tag': '_onAddParentTag',
            'click #add_group_tag': '_onAddGroupTag',
            'click #add_discipline_tag': '_onAddDisciplineTag',
        },
        _onAddDisciplineTag: function (ev) {
            console.log("discipline_tag");
            var tag_name = document.getElementById('tag_name').value;
            ajax.jsonRpc('/discipline_tag', 'call',{'tag_name': tag_name})
            .then(function (result) {
                var res = $('#tags');
                res.select2();
                var newOption = new Option(result.name, result.id, true, true);
                res.append(newOption).trigger('change');
                console.log($('#tag_name').val());
                $('#tag_name').val('');
                $('#addTagModal').modal('hide');

            });
        },

        _onAddFanTag: function (ev) {
            console.log('_onAddFanTag');
            var tag_name = document.getElementById('tag_name').value;
            ajax.jsonRpc('/fan_tag', 'call',{'tag_name': tag_name})
            .then(function(result) {
                var res = $('#tags');
                res.select2();
                var newOption = new Option(result.name, result.id, true, true);
                res.append(newOption).trigger('change');
                $('#tag_name').val('');
                $('#addTagModal').modal('hide');
            })
        },

        _onAddAthleteTag: function (ev) {
            console.log('_onAddAthleteTag');
            var tag_name = document.getElementById('tag_name').value;
            ajax.jsonRpc('/athlete_tag', 'call',{'tag_name': tag_name})
            .then(function(result) {
                var res = $('#tags');
                res.select2();
                var newOption = new Option(result.name, result.id, true, true);
                res.append(newOption).trigger('change');
                $('#tag_name').val('');
                $('#addTagModal').modal('hide');
            })
        },

        _onAddCoachTag: function (ev) {
            console.log('_onAddCoachTag');
            var tag_name = document.getElementById('tag_name').value;
            ajax.jsonRpc('/coach_tag', 'call',{'tag_name': tag_name})
            .then(function(result) {
                var res = $('#tags');
                res.select2();
                var newOption = new Option(result.name, result.id, true, true);
                res.append(newOption).trigger('change');
                $('#tag_name').val('');
                $('#addTagModal').modal('hide');
            })
        },

        _onAddVenueTag: function (ev) {
        console.log('_onAddVenueTag');
        var tag_name = document.getElementById('tag_name').value;
        ajax.jsonRpc('/venues_tag', 'call',{'tag_name': tag_name})
        .then(function(result) {
            var res = $('#tags');
            res.select2();
            var newOption = new Option(result.name, result.id, true, true);
            res.append(newOption).trigger('change');
            $('#tag_name').val('');
            $('#addTagModal').modal('hide');
            })
        },

        _onAddParentTag: function (ev) {
        console.log('_onAddParentTag');
        var tag_name = document.getElementById('tag_name').value;
        ajax.jsonRpc('/parents_tag', 'call',{'tag_name': tag_name})
        .then(function(result) {
            var res = $('#tags');
            res.select2();
            var newOption = new Option(result.name, result.id, true, true);
            res.append(newOption).trigger('change');
            $('#tag_name').val('');
            $('#addTagModal').modal('hide');
            })
        },

        _onAddGroupTag: function (ev) {
            console.log('_onAddGroupTag');
            var tag_name = document.getElementById('tag_name').value;
            ajax.jsonRpc('/group_tag', 'call',{'tag_name': tag_name})
            .then(function(result) {
                var res = $('#tags');
                res.select2();
                var newOption = new Option(result.name, result.id, true, true);
                res.append(newOption).trigger('change');
                $('#tag_name').val('');
                $('#addTagModal').modal('hide');
            })
        },
    });
});
