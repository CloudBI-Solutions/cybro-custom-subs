odoo.define('sports_erp_dashboard.coach', function (require) {
    "use strict";
    const dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var PortalSidebar = require('portal.PortalSidebar');
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var trow_count = 1
    var row_count = 11
    localStorage.setItem('trow_count',trow_count);
    localStorage.setItem('row_count',row_count);

    $(document).ready(function () {
      $('.sports-erp-dashbaord-select').select2();
    $("#event_tags").select2({tags:[]});
    $('input[name="datetimes"]').daterangepicker({
                                timePicker: true,
                                startDate: moment().startOf('hour'),
                                endDate: moment().startOf('hour').add(32, 'hour'),
                                locale: {
                                  format: 'YYYY-MM-DD HH:MM'
                                }
                              });
    });
//     $(".event_submit").click(function(ev) {
//        console.log("kkkkkkkkkkkkkkkkkk")
//        var ticket_lines = []
//        for(let i = 1; i <= trow_count; i++) {
//            if($("#product_" + i).val()){
//                ticket_lines.push({
//                product_id: $("#product_" + i).val(),
//                max: $("#max_" + i).val(),
//                name: $("#name_" + i).val(),
//                description: $("#description_" + i).val(),
//                start_date: $("#start_date_" + i).val(),
//                end_date: $("#end_date_" + i).val(),
//                price: $("#price_" + i).val()
//            })
//            }
//        }
//        console.log($('#event_name').val(),$('#website_menu').is(':checked'), $('#limit_reg'),$('#auto_confirm'),"lines")
//        ajax.jsonRpc('/update/event_template', 'call', {
//            ticket_lines: ticket_lines,
//            template: $('#template_id').val(),
//            name: $('#event_name').val(),
//            timezone: $('#time_zone').val(),
//            website_menu: $('#website_menu').is(':checked'),
//            register_button: $('#register_button').is(':checked'),
//            tags: $('#tags').val(),
//            limit_reg: $('#limit_reg').is(':checked'),
//            auto_confirm: $('#auto_confirm').is(':checked'),
//            notes: $('#notes').val(),
//            extra_info: $('#extra_info').val()
//            }).then(function(data){
//
//        })
//        location.reload();
//        console.log("data")
//    });

    publicWidget.registry.CoachPage = publicWidget.Widget.extend({
        selector: '.js_usermenu',
        events: {
            'click #organisations': '_onChangeOrganisation',
        },
        _onChangeOrganisation: function (ev) {
            utils.set_cookie('select_organisation', ev.currentTarget.value);
            console.log(document.cookie);
            location.reload();
        },
    });
    $("select[name='country_id']").change(function(){
                 var $select_state = $("select[name='state_id']");
                 $select_state.find("option:not(:first)").hide();
                 var nb = $select_state.find("option[data-country_id="+($(this).val() || 0)+"]").show().length;
                 $select_state.val(0);
    });
    publicWidget.registry.Booking = publicWidget.Widget.extend({
        selector: '#booking-form',
        events: {
               'change #booking_type': '_onChangeTypeId',
               'change #input_appointment_date': '_onChangeAppointmentDate',
    },
    _onChangeTypeId: function (ev) {
        console.log("1234567")
        $("input[id='input_appointment_date']").val(null);
        $('#schedules').empty();
        var type_selected = $("select[id='booking_type']").val();
        console.log(type_selected, "type")
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
        console.log("1234567")
        var date_selected = $("input[id='input_appointment_date']").val();
        console.log(date_selected)
        var coach_id = $("input[id='booking_coach_id']").val();
        var type_id = $("select[id='booking_type']").val();
        console.log(date_selected, type_id, coach_id)
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
});