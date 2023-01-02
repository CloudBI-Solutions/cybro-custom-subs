odoo.define('sports_erp_dashboard.booking', function (require) {
    "use strict";
    console.log("Kkkkkk")
    const dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var PortalSidebar = require('portal.PortalSidebar');
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var monday_trow_count = 1
    var tuesday_trow_count = 1
    var wednesday_trow_count = 1
    var thursday_trow_count = 1
    var friday_trow_count = 1
    var saturday_trow_count = 1
    var sunday_trow_count = 1
    localStorage.setItem('monday_trow_count',monday_trow_count);
    localStorage.setItem('tuesday_trow_count',tuesday_trow_count);
    localStorage.setItem('wednesday_trow_count',wednesday_trow_count);
    localStorage.setItem('thursday_trow_count',thursday_trow_count);
    localStorage.setItem('friday_trow_count',friday_trow_count);
    localStorage.setItem('saturday_trow_count',saturday_trow_count);
    localStorage.setItem('sunday_trow_count',sunday_trow_count);
    console.log('================================', localStorage, tuesday_trow_count)

    publicWidget.registry.Monday = publicWidget.Widget.extend({
        selector: '#profile',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#monday_table").find("tr") && $("#monday_table").find("tr").last()[0].id.split("_")[1]){
            monday_trow_count = parseInt($("#monday_table").find("tr").last()[0].id.split("_")[1])
        }
        monday_trow_count++;
        console.log(monday_trow_count, "trow")
        var row = "row_" + monday_trow_count
//        console.log(row_id, img_trow_count)
        var mon_from = "mon_from_" + monday_trow_count
        var mon_to = "mon_to_" + monday_trow_count
        console.log($("#monday_table"))
        $("#monday_table").append('<tr class="products" name="mon_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+mon_from+'" id="'+mon_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+mon_to+'" id="'+mon_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Tuesday = publicWidget.Widget.extend({
        selector: '#tuesdaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#tuesday_table").find("tr") && $("#tuesday_table").find("tr").last()[0].id.split("_")[2]){
            tuesday_trow_count = parseInt($("#tuesday_table").find("tr").last()[0].id.split("_")[2])
        }
        console.log(tuesday_trow_count)
        tuesday_trow_count++;
        console.log(tuesday_trow_count, "trow")
        var row = "tue_row_" + tuesday_trow_count
//        console.log(row_id, img_trow_count)
        var tue_from = "tue_from_" + tuesday_trow_count
        var tue_to = "tue_to_" + tuesday_trow_count
        console.log($("#tuesday_table"))
        $("#tuesday_table").append('<tr class="products" name="mon_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+tue_from+'" id="'+tue_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+tue_to+'" id="'+tue_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Wednesday = publicWidget.Widget.extend({
        selector: '#wednesdaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#wednesday_table").find("tr") && $("#wednesday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_trow_count = parseInt($("#wednesday_table").find("tr").last()[0].id.split("_")[2])
        }
        wednesday_trow_count++;
        console.log(wednesday_trow_count, "trow")
        var row = "wed_row_" + wednesday_trow_count
//        console.log(row_id, img_trow_count)
        var wed_from = "wed_from_" + wednesday_trow_count
        var wed_to = "wed_to_" + wednesday_trow_count
        console.log($("#tuesday_table"))
        $("#wednesday_table").append('<tr class="products" name="wed_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+wed_from+'" id="'+wed_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+wed_to+'" id="'+wed_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Thursday = publicWidget.Widget.extend({
        selector: '#thursdaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#thursday_table").find("tr") && $("#thursday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_trow_count = parseInt($("#thursday_table").find("tr").last()[0].id.split("_")[2])
        }
        thursday_trow_count++;
        var row = "thu_row_" + thursday_trow_count
//        console.log(row_id, img_trow_count)
        var thu_from = "thu_from_" + thursday_trow_count
        var thu_to = "thu_to_" + thursday_trow_count
        $("#thursday_table").append('<tr class="products" name="thu_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+thu_from+'" id="'+thu_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+thu_to+'" id="'+thu_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Friday = publicWidget.Widget.extend({
        selector: '#fridaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#friday_table").find("tr") && $("#friday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_trow_count = parseInt($("#friday_table").find("tr").last()[0].id.split("_")[2])
        }
        friday_trow_count++;
        console.log(wednesday_trow_count, "trow")
        var row = "fri_row_" + friday_trow_count
//        console.log(row_id, img_trow_count)
        var fri_from = "fri_from_" + friday_trow_count
        var fri_to = "fri_to_" + friday_trow_count
        $("#friday_table").append('<tr class="products" name="fri_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+fri_from+'" id="'+fri_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+fri_to+'" id="'+fri_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Saturday = publicWidget.Widget.extend({
        selector: '#saturdaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#saturday_table").find("tr") && $("#saturday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_trow_count = parseInt($("#saturday_table").find("tr").last()[0].id.split("_")[2])
        }
        saturday_trow_count++;
        console.log(wednesday_trow_count, "trow")
        var row = "sat_row_" + saturday_trow_count
//        console.log(row_id, img_trow_count)
        var sat_from = "sat_from_" + saturday_trow_count
        var sat_to = "sat_to_" + saturday_trow_count
        console.log($("#tuesday_table"))
        $("#saturday_table").append('<tr class="products" name="sat_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+sat_from+'" id="'+sat_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+sat_to+'" id="'+sat_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
    publicWidget.registry.Sunday = publicWidget.Widget.extend({
        selector: '#sundaytab',
        events: {
            'click #add_item': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#sunday_table").find("tr") && $("#sunday_table").find("tr").last()[0].id.split("_")[2]){
            wednesday_trow_count = parseInt($("#sunday_table").find("tr").last()[0].id.split("_")[2])
        }
        sunday_trow_count++;
        console.log(wednesday_trow_count, "trow")
        var row = "sun_row_" + sunday_trow_count
//        console.log(row_id, img_trow_count)
        var sun_from = "sun_from_" + sunday_trow_count
        var sun_to = "sun_to_" + sunday_trow_count
        console.log($("#tuesday_table"))
        $("#sunday_table").append('<tr class="products" name="sun_slot" id="'+row+'"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+sun_from+'" id="'+sun_from+'"/></td>
            <td class="td-product_name"><input type="text" name="'+sun_to+'" id="'+sun_to+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove" title="Remove" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },
    })
})