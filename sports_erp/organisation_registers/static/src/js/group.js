odoo.define('organisation_registers.group', function (require) {
    "use strict";
    const dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var PortalSidebar = require('portal.PortalSidebar');
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var monday_row_count = 1
    var tuesday_row_count = 1
    var wednesday_row_count = 1
    var thursday_row_count = 1
    var friday_row_count = 1
    var saturday_row_count = 1
    var sunday_row_count = 1
    localStorage.setItem('monday_row_count',monday_row_count);
    localStorage.setItem('tuesday_row_count',tuesday_row_count);
    localStorage.setItem('wednesday_row_count',wednesday_row_count);
    localStorage.setItem('thursday_row_count',thursday_row_count);
    localStorage.setItem('friday_row_count',friday_row_count);
    localStorage.setItem('saturday_row_count',saturday_row_count);
    localStorage.setItem('sunday_row_count',sunday_row_count);


    publicWidget.registry.Register = publicWidget.Widget.extend({
        selector: '#addRegistersModal',
        events: {
            'change #coach': '_onChangeCoach',
            'change #group': '_onChangeGroup',
//            'click .delete_image': '_onClickDeleteProduct'
        },
    _onChangeCoach: function(event){
        console.log("group", event)
         var $select_coach = $("#coach").val();
         var $select_group = document.querySelector('#group');
        $("#group").empty();
         console.log($select_coach, "coach...")
             ajax.jsonRpc('/get_groups', 'call', {
              'coach': $select_coach,
            }).then(function(data){
                console.log(data, "data")
                $('#group').append('<option>Choose Group</option>');
                for(let i = 0; i < data.groups.length; i++){
                    var option = new Option(data.groups[i][0], data.groups[i][1]);
                    console.log(option, "option")
                    $select_group.add(option);
                }
            })
    },
    _onChangeGroup: function(event){
        $('#athletes').empty()
        ajax.jsonRpc('/get_athletes', 'call', {
              'group': $('#group').val(),
            }).then(function(data){
                var element = document.getElementById('athletes');
                console.log(data, "data")
                if(data.athletes.length > 0){
                    for(let j = 0; j < data.athletes.length; j++){
                        var option = new Option(data.athletes[j][0],data.athletes[j][1],  true, true);
                        $('#athletes').append(option).trigger('change');

                        // manually trigger the `select2:select` event
                        $('#athletes').trigger({
                            type: 'select2:select',
//                            params: {
//                                data: data.athletes
//                            }
                        });
//                        $('#athletes').select2();
//                        $("#athletes").find("option[value="+data.athletes[j][0]+"]").prop("selected", "selected");
//                        var newOption = new Option(data.athletes[j][0],data.athletes[j][1]);
//                        console.log(newOption)
//                        $('#athletes').append(newOption);

                    }}

                else{
                    console.log("iii")
                    $('#athletes').val(null).trigger('change');
                }
                })
    },
    })

    publicWidget.registry.GroupMonday = publicWidget.Widget.extend({
        selector: '#monday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#monday_table").find("tr") && $("#monday_table").find("tr").last()[0].id.split("_")[1]){
            monday_row_count = parseInt($("#monday_table").find("tr").last()[0].id.split("_")[1])
        }
        monday_row_count++;
        console.log(monday_row_count, "trow")
        var row = "row_" + monday_row_count
//        console.log(row_id, img_trow_count)
        var mon_from = "mon_from_" + monday_row_count
        var mon_to = "mon_to_" + monday_row_count
        var mon_name = "mon_name_" + monday_row_count
        var mon_venue = "mon_venue_" + monday_row_count
        var mon_recurrent = "mon_recurrent_" + monday_row_count
        console.log($("#monday_table"))
        $("#monday_table").append('<tr name="mon_slot" id="'+row+'"><td class="td-product_name" name="mon_slot_name"><input type="text" class="form-control se-form-control" name="'+mon_name+'" id="'+mon_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+mon_venue+'" id="'+mon_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+mon_recurrent+'" id="'+mon_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+mon_from+'" id="'+mon_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+mon_to+'" id="'+mon_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+mon_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.TuesdayGroup = publicWidget.Widget.extend({
        selector: '#tuesday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#tuesday_table").find("tr") && $("#tuesday_table").find("tr").last()[0].id.split("_")[2]){
            tuesday_row_count = parseInt($("#tuesday_table").find("tr").last()[0].id.split("_")[2])
        }
//        console.log(tuesday_trow_count)
        tuesday_row_count++;
        console.log(tuesday_row_count, "trow")
        var row = "tue_row_" + tuesday_row_count
        var tue_from = "tue_from_" + tuesday_row_count
        var tue_to = "tue_to_" + tuesday_row_count
        var tue_name = "tue_name_" + tuesday_row_count
        var tue_venue = "tue_venue_" + tuesday_row_count
        var tue_recurrent = "tue_recurrent_" + tuesday_row_count
        $("#tuesday_table").append('<tr name="tue_slot" id="'+row+'"><td class="td-product_name" name="tue_slot_name"><input type="text" class="form-control se-form-control" name="'+tue_name+'" id="'+tue_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+tue_venue+'" id="'+tue_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+tue_recurrent+'" id="'+tue_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+tue_from+'" id="'+tue_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+tue_to+'" id="'+tue_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+tue_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.WednesdayGroup = publicWidget.Widget.extend({
        selector: '#wednesday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#wednesday_table").find("tr") && $("#wednesday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_row_count = parseInt($("#wednesday_table").find("tr").last()[0].id.split("_")[2])
        }
        wednesday_row_count++;
        var row = "wed_row_" + wednesday_row_count
        var wed_from = "wed_from_" + wednesday_row_count
        var wed_to = "wed_to_" + wednesday_row_count
        var wed_name = "wed_name_" + wednesday_row_count
        var wed_venue = "wed_venue_" + wednesday_row_count
        var wed_recurrent = "wed_recurrent_" + wednesday_row_count
        $("#wednesday_table").append('<tr name="wed_slot" id="'+row+'"><td class="td-product_name" name="wed_slot_name"><input type="text" class="form-control se-form-control" name="'+wed_name+'" id="'+wed_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+wed_venue+'" id="'+wed_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+wed_recurrent+'" id="'+wed_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+wed_from+'" id="'+wed_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+wed_to+'" id="'+wed_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+wed_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.ThursdayGroup = publicWidget.Widget.extend({
        selector: '#thursday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#thursday_table").find("tr") && $("#thursday_table").find("tr").last()[0].id.split("_")[2]){
            thursday_row_count = parseInt($("#thursday_table").find("tr").last()[0].id.split("_")[2])
        }
        thursday_row_count++;
        var row = "thu_row_" + thursday_row_count
        var thu_from = "thu_from_" + thursday_row_count
        var thu_to = "thu_to_" + thursday_row_count
        var thu_name = "thu_name_" + thursday_row_count
        var thu_venue = "thu_venue_" + thursday_row_count
        var thu_recurrent = "thu_recurrent_" + thursday_row_count
        $("#thursday_table").append('<tr name="thu_slot" id="'+row+'"><td class="td-product_name" name="thu_slot_name"><input type="text" class="form-control se-form-control" name="'+thu_name+'" id="'+thu_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+thu_venue+'" id="'+thu_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+thu_recurrent+'" id="'+thu_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+thu_from+'" id="'+thu_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+thu_to+'" id="'+thu_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+thu_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })

    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.FridayGroup = publicWidget.Widget.extend({
        selector: '#friday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#friday_table").find("tr") && $("#friday_table").find("tr").last()[0].id.split("_")[2]){
            friday_row_count = parseInt($("#friday_table").find("tr").last()[0].id.split("_")[2])
        }
        friday_row_count++;
        console.log(friday_row_count, "trow")
        var row = "fri_row_" + friday_row_count
        var fri_from = "fri_from_" + friday_row_count
        var fri_to = "fri_to_" + friday_row_count
        var fri_name = "fri_name_" + friday_row_count
        var fri_venue = "fri_venue_" + friday_row_count
        var fri_recurrent = "fri_recurrent_" + friday_row_count
        $("#friday_table").append('<tr name="fri_slot" id="'+row+'"><td class="td-product_name" name="fri_slot_name"><input type="text" class="form-control se-form-control" name="'+fri_name+'" id="'+fri_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+fri_venue+'" id="'+fri_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+fri_recurrent+'" id="'+fri_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+fri_from+'" id="'+fri_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+fri_to+'" id="'+fri_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+fri_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.SaturdayGroup = publicWidget.Widget.extend({
        selector: '#saturday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#saturday_table").find("tr") && $("#saturday_table").find("tr").last()[0].id.split("_")[2]){
            saturday_row_count = parseInt($("#saturday_table").find("tr").last()[0].id.split("_")[2])
        }
        saturday_row_count++;
        var row = "sat_row_" + saturday_row_count
        var sat_from = "sat_from_" + saturday_row_count
        var sat_to = "sat_to_" + saturday_row_count
        var sat_name = "sat_name_" + saturday_row_count
        var sat_venue = "sat_venue_" + saturday_row_count
        var sat_recurrent = "sat_recurrent_" + saturday_row_count
        $("#saturday_table").append('<tr name="sat_slot" id="'+row+'"><td class="td-product_name" name="sat_slot_name"><input type="text" class="form-control se-form-control" name="'+sat_name+'" id="'+sat_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+sat_venue+'" id="'+sat_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+sat_recurrent+'" id="'+sat_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+sat_from+'" id="'+sat_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+sat_to+'" id="'+sat_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+sat_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })

    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.SundayGroup = publicWidget.Widget.extend({
        selector: '#sunday_tab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#sunday_table").find("tr") && $("#sunday_table").find("tr").last()[0].id.split("_")[2]){
            sunday_row_count = parseInt($("#sunday_table").find("tr").last()[0].id.split("_")[2])
        }
        sunday_row_count++;
        console.log(sunday_row_count, "trow")
        var row = "sun_row_" + sunday_row_count
        var sun_from = "sun_from_" + sunday_row_count
        var sun_to = "sun_to_" + sunday_row_count
        var sun_name = "sun_name_" + sunday_row_count
        var sun_venue = "sun_venue_" + sunday_row_count
        var sun_recurrent = "sun_recurrent_" + sunday_row_count
        $("#sunday_table").append('<tr name="sun_slot" id="'+row+'"><td class="td-product_name" name="sun_slot_name"><input type="text" class="form-control se-form-control" name="'+sun_name+'" id="'+sun_name+'"/></td>
            <td><select class="form-control se-form-control"  name="'+sun_venue+'" id="'+sun_venue+'"><option></option></select></td>
            <td class="td-product_name"><label class="switch"><input type="checkbox" name="'+sun_recurrent+'" id="'+sun_recurrent+'" class="form-control se-form-control"/><span class="slider round"></span>
                                                    </label></td>
            <td class="td-product_name"><input type="time" name="'+sun_from+'" id="'+sun_from+'" class="form-control se-form-control"/></td>
            <td class="td-product_name"><input type="time" name="'+sun_to+'" id="'+sun_to+'" class="form-control se-form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
        var venues = document.querySelector('#'+sun_venue);
             ajax.jsonRpc('/get_venues', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.venues.length; i++){
                    var option = new Option(data.venues[i][0], data.venues[i][1]);
                    venues.add(option);
                }
            })

    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
})