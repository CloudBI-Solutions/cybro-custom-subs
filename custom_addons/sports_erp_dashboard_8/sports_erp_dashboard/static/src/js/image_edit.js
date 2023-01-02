odoo.define('sports_erp_dashboard.home_image', function (require) {
    "use strict";

    const dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var PortalSidebar = require('portal.PortalSidebar');
    var utils = require('web.utils');
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var img_trow_count = 1
    var row_count = 11
    localStorage.setItem('img_trow_count',img_trow_count);
    localStorage.setItem('row_count',row_count);

    publicWidget.registry.ImageEditTemplate = publicWidget.Widget.extend({
        selector: '.image_edit_template',
        events: {
//            'click .update_image': '_onEventSubmit',
            'click #add_image': '_onAddItem',
            'click .delete_image': '_onClickDeleteProduct'
        },
        _onEventSubmit: async function (ev) {
        console.log("haiiii");

//            if ($('#number').val()){
//                img_trow_count = $('#number').val()
//            }
            var image_lines = []
        for(let i = 1; i <= img_trow_count; i++) {
            console.log($("#image_" + i).val(), "llll")
            if($("#image_" + i).val()){
            const file = document.querySelector("#image_" + i).files[0];
            var fileReader = new FileReader();
                fileReader.onload = function () {
                  var data = fileReader.result;  // data <-- in this var you have the file data in Base64 format
                };
//                fileReader.readAsDataURL(file);
//                console.log('fR', fileReader.result)
                console.log(fileReader.readAsBinaryString(file))
            if($("#name_" + i).val()){
                image_lines.push({
                name: $("#name_" + i).val(),
                image: fileReader,
                description: $("#description_" + i).val(),

            })
            }
        }
        console.log(image_lines)
        ajax.jsonRpc('/update/image_template', 'call', {
            image_lines: image_lines,
        }).then(function(data){
            console.log(data)
        })
//           try {
//                console.log(file, "file")
//              const result = await toBase64(file);
//              return result
//           } catch(error) {
//              console.error(error);
//              return;
//           }
            }


//        location.reload();

    },
    _onAddItem: function(event){
    console.log('byeee');

        var number = $('#number').val();
        if (number){
            img_trow_count = parseInt(number)
        }
        var row_id = "row_" + img_trow_count
        console.log(row_id)
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
            img_trow_count++;
//            var product_items = document.querySelector('#'+product_id);
//             ajax.jsonRpc('/get_products', 'call', {
//            }).then(function(data){
//                for(let i = 0; i < data.product_ids.length; i++){
//                    var option = new Option(data.product_ids[i][0], data.product_ids[i][1]);
//                    product_items.add(option);
//                }
//            })
    },
    _onClickDeleteProduct: function(e) {
        var row =  $(e.currentTarget).parent().parent()[0].id
        console.log(row)
        $('#'+row).remove();

    },

    })
    })