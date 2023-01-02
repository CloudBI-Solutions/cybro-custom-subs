odoo.define('sports_erp_dashboard.events', function (require) {
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

    publicWidget.registry.EventsTemplate = publicWidget.Widget.extend({
        selector: '.events_template',
        events: {
            'click .event_submit': '_onEventSubmit',
            'click #add_item': '_onAddItem',
            'click .delete_product': '_onClickDeleteProduct'
        },
        _onEventSubmit: function (ev) {

            if ($('#number').val()){
                trow_count = $('#number').val()
            }
            var ticket_lines = []
        for(let i = 1; i <= trow_count; i++) {
            if($("#product_" + i).val()){
                ticket_lines.push({
                product_id: $("#product_" + i).val(),
                max: $("#max_" + i).val(),
                name: $("#name_" + i).val(),
                description: $("#description_" + i).val(),
                start_date: $("#start_date_" + i).val(),
                end_date: $("#end_date_" + i).val(),
                price: $("#price_" + i).val()
            })
            }
        }
        ajax.jsonRpc('/update/event_template', 'call', {
            ticket_lines: ticket_lines,
            template: $('#template_id').val(),
            name: $('#event_name').val(),
            timezone: $('#time_zone').val(),
            website_menu: $('#website_menu').is(':checked'),
            register_button: $('#register_button').is(':checked'),
            tags: $('#tags').val(),
            limit_reg: $('#limit_reg').is(':checked'),
            auto_confirm: $('#auto_confirm').is(':checked'),
            notes: $('#notes').val(),
            extra_info: $('#extra_info').val()
            }).then(function(data){

        })
        location.reload();

    },
    _onAddItem: function(event){
        trow_count++;
        var number = $('#number').val();
        if (number){
            trow_count = parseInt(number) + 1
        }
        var row_id = "row_" + trow_count
        var product_id = "product_" + trow_count
        var name = "name_" + trow_count
        var quantity = "qty_" + trow_count
        var description = "description_" + trow_count
        var price = "price_" + trow_count
        var start_date = "start_date_" + trow_count
        var end_date = "end_date_" + trow_count
        var max = "max_" + trow_count
        $("#add_products").append('<tr id="'+row_id+'" class="products"><td class="td-product_name" name="ticket_name"><input type="text" class="form-control" name="ticket_name" id="'+name+'"/></td><td class="td-product_name"><select class="form-control select_products"  name="product_select" id="'+product_id+'"><option></option></select></td>
            <td class="td-product_name"><input type="text" name="ticket_description" id="'+description+'" class="form-control"/></td>
            <td class="td-product_name"><input type="number" name="price" id="'+price+'" class="form-control"/></td>
            <td class="td-product_name"><input type="number" name="max" id="'+max+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove from cart" title="Remove from cart" class="delete_product no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
            </td>
            </tr>'
            );
            var product_items = document.querySelector('#'+product_id);
             ajax.jsonRpc('/get_products', 'call', {
            }).then(function(data){
                for(let i = 0; i < data.product_ids.length; i++){
                    var option = new Option(data.product_ids[i][0], data.product_ids[i][1]);
                    product_items.add(option);
                }
            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        $('#'+row).remove();

    },

    })
    })