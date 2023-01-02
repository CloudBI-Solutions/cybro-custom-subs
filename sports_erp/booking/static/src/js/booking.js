odoo.define('booking.dashboard', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    console.log("Booking")
    $(document).ready(function(){
        $('#public_user_creation_form').hide();
        var date_selected = $("input[id='input_appointment_date']").val();
        var coach_id = $("input[id='booking_coach_id']").val();
        var type_id = $("select[id='type_id']").val();
        $('#schedules').empty();
        $('#public_schedules').empty();
        if(date_selected && type_id && coach_id){
        ajax.jsonRpc('/get_coach_schedule', 'call',{'date': date_selected, 'coach_id': coach_id, 'type_id': type_id})
            .then(function (result) {
                    if(result.schedule.length > 0){
                    for (var i=0; i<result.schedule.length; i++){
                        $('#schedules').append('<div class="col-4 col-sm-4 col-md-3 col-lg-2 p-2"><input type="radio" name="slot" value="'+ result.schedule[i].time +'"><label><span>' + result.schedule[i].slot +'</span></label></div><br>');
                    }
                }
                else{
                    $('#schedules').append('<div class="alert alert-warning mt8" role="alert">No Slots found!!</div>');
                }
            });
        }
        $('#hide_related_bookings').hide();
        var appointment_type = $("select[id='type_selected']").val();
        if(appointment_type){
            ajax.jsonRpc('/get_booking_values', 'call',{'type_id': appointment_type})
                .then(function (result) {
                    $('#duration').val(result.duration);
                    $('#venue').val(result.venue);
                    $('#coach').val(result.coach);
                    $('#coach_id').val(result.coach_id);
                });
        }
        var type_selected = $("select[id='type_id']").val();
        if (type_selected){
            ajax.jsonRpc('/get_booking_values', 'call',{'type_id': type_selected})
                .then(function (result) {
                    $('#input_duration').val(result.duration);
                    $('#input_coach').val(result.coach);
                    $('#input_venue').val(result.venue);
                });
        }

        var public_type_selected = $("select[id='public_type_id']").val();
        if (public_type_selected){
            ajax.jsonRpc('/get_public_booking_values', 'call',{'type_id': public_type_selected})
                .then(function (result) {
                    $('#public_input_duration').val(result.duration);
                    $('#public_input_coach').val(result.coach);
                    $('#public_input_venue').val(result.venue);
                });
        }

    });


    publicWidget.registry.Dashboard = publicWidget.Widget.extend({
        selector: '#type',
        events: {
               'change #type_selected': '_onChangeType',
    },
    _onChangeType: function (ev) {
        var appointment_type = $("select[id='type_selected']").val();
        if(appointment_type){
        $('#view_schedule_button').show();
        ajax.jsonRpc('/get_booking_values', 'call',{'type_id': appointment_type})
            .then(function (result) {
                $('#duration').val(result.duration);
                $('#venue').val(result.venue);
                $('#coach').val(result.coach);
                $('#coach_id').val(result.coach_id);
            });
        }
        else{
            $('#view_schedule_button').hide()
            $('#duration').val(null);
            $('#venue').val(null);
            $('#coach').val(null);
            $('#coach_id').val(null);
        }
    },

    });

    publicWidget.registry.CreateBooking = publicWidget.Widget.extend({
        selector: '#submit_form',
        events: {
               'change #type_id': '_onChangeTypeId',
               'change #input_appointment_date': '_onChangeAppointmentDate',
    },
    _onChangeTypeId: function (ev) {
        $("input[id='input_appointment_date']").val(null);
        $('#schedules').empty();
        var type_selected = $("select[id='type_id']").val();
        if(type_selected){
        $('#view_coach_schedule').show();
        ajax.jsonRpc('/get_booking_values', 'call',{'type_id': type_selected})
            .then(function (result) {
                $('#input_duration').val(result.duration);
                $('#input_coach').val(result.coach);
                $('#booking_coach_id').val(result.coach_id);
                $('#input_venue').val(result.venue);
            });
        }
        else{
            $('#view_coach_schedule').hide();
            $('#input_duration').val(null);
            $('#input_coach').val(null);
            $('#booking_coach_id').val(null);
            $('#input_venue').val(null);
        }
    },

    _onChangeAppointmentDate: function (ev) {
        var date_selected = $("input[id='input_appointment_date']").val();
        var coach_id = $("input[id='booking_coach_id']").val();
        var type_id = $("select[id='type_id']").val();
        $('#schedules').empty();
        if(date_selected && type_id && coach_id){
        ajax.jsonRpc('/get_coach_schedule', 'call',{'date': date_selected, 'coach_id': coach_id, 'type_id': type_id})
            .then(function (result) {
                    if(result.schedule.length > 0){
                    for (var i=0; i<result.schedule.length; i++){
                        $('#schedules').append('<div class="col-4 col-sm-4 col-md-3 col-lg-2 p-2"><input id="'+ i +'" type="radio" name="slot" value="'+ result.schedule[i].time +'"><label for="'+ i +'"><span>' + result.schedule[i].slot +'</span></label></input></div><br>');
                    }
                }
                else{
                    $('#schedules').append('<div class="alert alert-warning mt8" role="alert">No Slots found!!</div>');
                }
            });
        }

    },

    });

    publicWidget.registry.CreatePublicBooking = publicWidget.Widget.extend({
        selector: '#public_submit_form',
        events: {
               'change #public_type_id': '_onChangePublicTypeId',
               'change #public_input_appointment_date': '_onChangePublicAppointmentDate',
    },
    _onChangePublicTypeId: function (ev) {
        $("input[id='public_input_appointment_date']").val(null);
        $('#public_schedules').empty();
        var type_selected = $("select[id='public_type_id']").val();
        if(type_selected){
        ajax.jsonRpc('/get_public_booking_values', 'call',{'type_id': type_selected})
            .then(function (result) {
                $('#public_input_duration').val(result.duration);
                $('#public_input_coach').val(result.coach);
                $('#public_input_venue').val(result.venue);
            });
        }
        else{
            $('#input_duration').val(null);
            $('#input_coach').val(null);
            $('#input_venue').val(null);
        }
    },

    _onChangePublicAppointmentDate: function (ev) {
        var date_selected = $("input[id='public_input_appointment_date']").val();
        var type_id = $("select[id='public_type_id']").val();
        $('#public_schedules').empty();
        if(date_selected && type_id){
        ajax.jsonRpc('/get_coach_schedule_public', 'call',{'date': date_selected, 'type_id': type_id})
            .then(function (result) {
                    if(result.schedule.length > 0){
                    for (var i=0; i<result.schedule.length; i++){
                        $('#public_schedules').append('<div class="col-4 col-sm-4 col-md-3 col-lg-2 p-2"><input class="button-public-slot" id="'+ i +'" type="radio" name="public_slot" value="'+ result.schedule[i].time +'"><label for="'+ i +'"><span>' + result.schedule[i].slot +'</span></label></input></div><br>');
                    }
                }
                else{
                    $('#public_schedules').append('<div class="alert alert-warning mt8" role="alert">No Slots found!!</div>');
                }
            });
        }

    },

    });

//    publicWidget.registry.CreatePublicBookingConfirm = publicWidget.Widget.extend({
//        selector: '#div_button_confirm_schedule',
//        events: {
//               'click #button_confirm_schedule': '_onClickSlotConfirmButton',
//        },
//        _onClickSlotConfirmButton: function (ev) {
//        var user_name = $("input[id='user_name']").val();
//        var user_email = $("input[id='user_email']").val();
//        var date_selected = $("input[id='public_input_appointment_date']").val();
//        var type_id = $("select[id='public_type_id']").val();
//        var slot = $("input[type=radio][name=public_slot]:checked").val()
//        if (slot){
//        ajax.jsonRpc('/create_public_booking', 'call',{'date': date_selected, 'type_id': type_id, 'slot': slot, 'user_name': user_name, 'user_email': user_email})
//        }
//        else{
//            alert("Please select slot")
//
//        }
////        ajax.jsonRpc('/create_public_booking', 'call',{'date': date_selected, 'type_id': type_id, 'slot': slot, 'user_name': user_name, 'user_email': user_email})
////        $('#public_user_creation_form').show();
//    },
//    });
    publicWidget.registry.RelatedBooking = publicWidget.Widget.extend({
        selector: '#related_booking_button',
        events: {
               'click #show_related_bookings': '_onClickShowRelatedBookingButton',
               'click #hide_related_bookings': '_onClickHideRelatedBookingButton',
    },
    _onClickShowRelatedBookingButton: function (ev) {
        $('#show_related_bookings').hide();
        $('#hide_related_bookings').show();
        $('#related_bookings').show();
    },
    _onClickHideRelatedBookingButton: function (ev) {
        $('#show_related_bookings').show();
        $('#hide_related_bookings').hide();
        $('#related_bookings').hide();
    },
    });

});
