odoo.define('sports_erp_dashboard.home_image', function (require) {
    "use strict";

    const dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var PortalSidebar = require('portal.PortalSidebar');
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var img_trow_count = 1
    var gallery_row_count = 1
    localStorage.setItem('img_trow_count',img_trow_count);
    localStorage.setItem('gallery_row_count',gallery_row_count);

    publicWidget.registry.ImageEditTemplate = publicWidget.Widget.extend({
        selector: '.image_edit_template',
        events: {
            'click #add_image': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddItem: function(event){
        if($("#image_table").find("tr").last()[0].id.split("_")[1]){
            img_trow_count = parseInt($("#image_table").find("tr").last()[0].id.split("_")[1])
        }
        img_trow_count++;
        var row_id = "row_" + img_trow_count
        console.log(row_id, img_trow_count)
        var product_id = "product_" + img_trow_count
        var name = "name_" + img_trow_count
        var image = "image_" + img_trow_count
        var description = "description_" + img_trow_count
        var price = "price_" + img_trow_count
        var start_date = "start_date_" + img_trow_count
        var end_date = "end_date_" + img_trow_count
        var max = "max_" + img_trow_count
        $("#image_table").append('<tr id="'+row_id+'" class="products"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+name+'" id="'+name+'"/></td>
            <td class="td-product_name"><input type="file" name="'+image+'" id="'+image+'" class="form-control"/></td>
            <td class="td-product_name"><input type="text" name="'+description+'" id="'+description+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove from cart" title="Remove from cart" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
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
    publicWidget.registry.GalleryImageEdit = publicWidget.Widget.extend({
        selector: '.gallery_images',
        events: {
            'click #add_item': '_onAddAnItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
    _onAddAnItem: function(event){
        console.log("Added")
        if($("#gallery_images").find("tr").last()[0].id.split("_")[1]){
            gallery_row_count = parseInt($("#gallery_images").find("tr").last()[0].id.split("_")[1])
        }
        gallery_row_count++;
        var row_id = "row_" + gallery_row_count
        var image = "image_" + gallery_row_count
        var name = "name_" + gallery_row_count
        $("#gallery_images").append('<tr id="'+row_id+'" class="products"><td class="td-product_name" name="home_name"><input type="text" class="form-control" name="'+name+'" id="'+name+'"/></td>
            <td class="td-product_name"><input type="file" name="'+image+'" id="'+image+'" class="form-control"/></td>
            <td class="td-action">
                <a href="#" aria-label="Remove from cart" title="Remove from cart" class="delete_image no-decoration"> <small><i class="fa fa-trash-o"></i></small></a>
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